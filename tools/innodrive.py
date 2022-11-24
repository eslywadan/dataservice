# from asyncio.log import logger
# from http.client import LineTooLong
from pickle import FALSE, TRUE
# from re import L
import string
# from tkinter.messagebox import NO
# from typing import Dict
from tools.config_loader import ConfigLoader
from tools.sec_loader import SecretLoader
from tools.logger import Logger
import requests
import base64
import os
import time
import json
import math
import re


class Irequests():
    """The class is designed for improving the interoperability with innodrive.
    The first implementation is the handling of RPM, it will wait till the next available cycle whever the RPM is reached.
    """

    m0 = '{"status":500,"message":"API Call 超過 RPM 次數限制 RPM=20, 週期剩餘時間TTL=59.075 sec."}'
    m1 = 'API Call 超過 RPM 次數限制'
    m2 = 'TTL='
    m3 = 'RPM='
    m4 = '{"status":500,"message":"Error: contains invalid characters  \\\\/:*?\\"<>| "}'
    m5 = '{"status":500,"message":"00001: unique constraint (INXDRV_DB.AK_DOC_FILES01) violated"}'

    def __init__(self):
        """Whenever the object is init, the cached requests is reset"""
        self.reset_cached_req()

    def reset_cached_req(self):
        """ The cached request is storing the accumulated requests since the reseted start time
            The requests uri and the accumulated count will be stored. The cached content is usually
            rested on (1) object is init (2) Over 'RPM' constraint
        """
        self.cached_req = []
        self.reset_stime = time.ctime()
        self.accum_req = 0

    def post(self, url, headers=None,json=None,data=None,files=None,recall=False):

        if recall:print(f"resume request for {url}, current time {time.ctime()}")
        resp = requests.post(url,headers=headers,json=json,data=data,files=files)
        if resp.status_code == 200:
            self.cached_req.append(f'Request api: {url} headers: {headers} json: {json} data: {data} files: {files} Sucess @Response time:{time.ctime()}\n')
            self.accum_req += 1
            return resp
        elif resp.status_code == 500 and self.parse_wait(resp.text) == 'wait':  # case when over the RPM wait till next cycle:
            Logger.log(f"Wait {self.m1} Start time {self.reset_stime}")   
            Logger.log(f"past requests:{self.cached_req}")                      # cached requests is dumped for tracing 
            Logger.log(f"accumulated req count: {self.accum_req}")
            self.reset_cached_req()
            self.wait_till()
            return self.post(url,headers=headers, json=json,data=data,files=files, recall=True)
        else:
            return resp
    
    def get(self, url, headers=None,recall=False):
        if recall:print(f"resume request for {url}, current time {time.ctime()}")
        resp = requests.get(url,headers=headers)
        if resp.status_code == 200:
            self.cached_req.append(f'Request api : {url} headers: {headers} Sucess @Response time:{time.ctime()}')
            self.accum_req += 1
            return resp
        elif resp.status_code == 500 and self.parse_wait(resp.text) == 'wait':  # case when over the RPM wait till next cycle
            Logger.log(f"{self.m1} Start time {self.reset_stime}")
            Logger.log(f"past requests:{self.cached_req}")
            Logger.log(f"accumulated req count: {self.accum_req}")
            self.reset_cached_req()
            self.wait_till()
            return self.get(url,header=headers,recall=True)        
        else:
            return resp

    def wait_till(self):
        #Logger.log(f"wait till next avaiable / current time {time.ctime()}")
        # print(f"{text} wait till next avaiable /current time {time.ctime()}")
        time.sleep(math.ceil(self.wait+1))

    def parse_wait(self,msg:string):
        """"Due to status code 500 has other server error casaes, It needs to validate the RPM violation case via the message.  """
        mi = re.search(self.m2,msg)
        mj = re.search(self.m3,msg)
        if mi or mj is None: return None
        self.wait = float(msg[mi.span()[1]:mi.span()[1]+6])
        return "wait"

class InnoDrive():
   
    _inodrvhost = ConfigLoader.config("innodrive")["innodrive_apattach"]
    _apikey_dur = ConfigLoader.config("innodrive")["apikey_dur"]
    _getkey_timeout = ConfigLoader.config("innodrive")["getkey_timeout"]
    _nodeid = ConfigLoader.config("innodrive")["nodeid"]
    _tempfold = ConfigLoader.config("innodrive")["tempfold"]
    _clientstore = ConfigLoader.config("innodrive")["clientstore"]
    _apilist = ConfigLoader.config("innodrive_api")
    _level1 = ConfigLoader.config("innodrive_datastudio")
    _identity = SecretLoader.secret("innodrive")
    
    _get_apikey_url = '%s%s' % (_inodrvhost, _apilist["getapiticket"])
    _get_items_url = '%s%s' % (_inodrvhost, _apilist["getitems"])
    _get_download_file_url = '%s%s' % (_inodrvhost, _apilist["getdownloadfileurl"])
    _upload_files_url = '%s%s' % (_inodrvhost, _apilist["uploadfiles"])
    _add_folder_url = '%s%s' % (_inodrvhost, _apilist["addfolder"])
    _delete_file_url = '%s%s' % (_inodrvhost, _apilist["deletefile"])
    _rename_url = '%s%s' % (_inodrvhost, _apilist["rename"])
    _get_item_tree_url = '%s%s' % (_inodrvhost, _apilist["getitemtree"])

    _apikey_st = time.monotonic()  #API Key Start Time. init with the current monotonic time
    
    idname = {}
    idbyte = {}
    idtype = {}
    idparent = {}
    idpath = {}
    nameids = {}
    iditemsid = {}
    iditemsname = {}

    irequests = Irequests()
    
    def __init__(self,clientid=None):
        """
        if clientds is True, the init object will only have the client's info 
        """
        self.get_apikey()
        if clientid is not None: self.set_client_items_all(clientid)
        else: self.set_node_items_all()

    
    def get_apikey(self):

        self.apikey = None   # Firstly, reset the APIKey to None
        payload = {'Account' : self._identity["NODEID"], 'Password' : self._identity["CRED"]}
        resp = InnoDrive.irequests.post(InnoDrive._get_apikey_url, json=payload)
        
        if resp.status_code == 200:
            self.apikey = resp.text.strip('"')
            self._apikey_st = time.monotonic()  # Reset the stat time
            Logger.log(f"Request get_apiticket from {self._get_apikey_url} with retrun code {resp.status_code} / get_ticket {self.apikey}")  
        
        else:
            Logger.log(f"Request get_apiticket from {self._get_apikey_url} with retrun code {resp.status_code} / fail on get_ticket {resp.text}") 
    
    
    def val_apikey(self):
        """Check the lifetime of the apikey. The life time is current time - start time of the apikey. 
        If the life time is longer than the config duration, the apikey is expected to be obsolete and needs to get a new key """

        st = time.monotonic()
        while time.monotonic() - self._apikey_st > self._apikey_dur or self.apikey == None:
            Logger.log(f"{self.apikey} is obsolete, renew the apikey") 
            self.get_apikey()
            if self.apikey is not None:
                Logger.log(f"A renew API Key is got {self.apikey} ")
            if time.monotonic() - st > 10 and self.apikey is None:
                Logger.log(f"Cannot renew API Key !")
            

    def get_items(self,objid, valapikey=TRUE):
        """accept the object id and return the items belong to the object id  """
        if valapikey: self.val_apikey()   # Validate an API Key
        elif self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return None

        payload = {"parentId":objid}
        headers = {"ticket": self.apikey}
        resp = InnoDrive.irequests.post(self._get_items_url,json=payload, headers=headers)
        if resp.status_code == 200:
            Logger.log(f"Request get_items from {self._get_items_url} with retrun code {resp.status_code} / get_items {resp.text}")  
        else:
            print(f"Request get_items from {self._get_items_url} with retrun code {resp.status_code} / fail on get_items {resp.text}")
            Logger.log(f"Request get_items from {self._get_items_url} with retrun code {resp.status_code} / fail on get_items {resp.text}") 

        return resp

    def get_item_tree(self,objid, valapikey=TRUE):
        """accept the object id and return the items belong to the object id  """
        if valapikey: self.val_apikey()   # Validate an API Key
        elif self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return None

        payload = {"parentId":objid}
        headers = {"ticket": self.apikey}
        resp = InnoDrive.irequests.post(self._get_item_tree_url,json=payload, headers=headers)
        if resp.status_code == 200:
            Logger.log(f"Request get_item_tree from {self._get_item_tree_url} with retrun code {resp.status_code} / get_items {resp.text}")  
        else:
            print(f"Request get_items from {self._get_item_tree_url} with retrun code {resp.status_code} / fail on get_items {resp.text}")
            Logger.log(f"Request get_items from {self._get_item_tree_url} with retrun code {resp.status_code} / fail on get_items {resp.text}") 

        return resp

    def read_item_tree(self,itree:dict,objid):
        self.iditemsid[objid] = []
        self.iditemsname[objid] = []
        for branch in itree:
            self.idname[branch['fileID']] = branch['name']
            self.idtype[branch['fileID']] = branch['type']
            self.idparent[branch['fileID']] = branch['parentID']
            self.idbyte[branch['fileID']] = branch['bytes']
            self.nameaddid(branch['fileID'], branch['name'])
            self.iditemsid[objid].append(branch['fileID'])
            self.iditemsname[objid].append(branch['name'])
            if branch['type'] == 'D' and len(branch['children']) > 0:
                self.read_item_tree(branch['children'],branch['fileID'])

    def set_items_all_by_tree(self, objid,valapikey=TRUE):
        resp = self.get_item_tree(objid)
        if resp.status_code != 200:return {"status":resp.status_code,"messsage":resp.text}
        self.iditemsid[objid] = []
        self.iditemsname[objid] = []
        self.idname[objid] = resp.json()['name']
        self.idtype[objid] = resp.json()['type']
        self.idparent[objid] = resp.json()['parentID']
        self.idbyte[objid] = resp.json()['bytes']
        itree = resp.json()['children']
        if len(itree) > 0 : self.read_item_tree(itree, objid)

    def set_items_all(self, objid,valapikey=TRUE,deep=TRUE):
        """The function 'set_items_all' will loop and deep into item whose type is 'D',
            it indicates the item is a folder. 
            It is expected to be called when a new instance is initialized.
            If the deep code is false, it wil not deep"""

        items = self.get_items(objid,valapikey)
        itemids = []
        namesids = []
        for item in items.json():
            if item['type'] == 'D' and deep:
                self.set_items_all(item['id'],valapikey)
            self.idname[item['id']] = item['name']
            self.idtype[item['id']] = item['type']
            self.idparent[item['id']] = item['parentId']
            self.idbyte[item['id']] = item['bytes']
            self.nameaddid(item['id'],item['name'])
            itemids.append(item['id'])
            namesids.append(item['name'])

        """keep the record of items by id which is belong to the parent"""

        self.iditemsid[objid] = itemids  

        """Keep the record of items by name which is belong to the parent"""
        self.iditemsname[objid] = namesids

    def add_items_2levels(self, parentobjid, objid, valapikey=TRUE):
        """The function 'add_items_single' will loop items and will not deep into element like set_items_all. 
            It is expected to be called 
            1. Upload a new file or create a new folder 
            the parent of the obj must be reset (pass the parent id & objid)
            Note that the update condition is required when the elem id = obj id
            """
        items = self.get_items(parentobjid,valapikey)
        for item in items.json():
            if item['id'] == objid:
                self.idname[item['id']] = item['name']
                self.idtype[item['id']] = item['type']
                self.idparent[item['id']] = item['parentId']
                self.idbyte[item['id']] = item['bytes']
                self.nameaddid(item['id'], item['name'])

    def deduct_items_single(self, objid, objname, valapikey=TRUE):
        """The function 'deduct_items_single' will deduct items from idname, idtype, idparent, idtype & nameids. 
            It is expected to be called 
            2. Delete a file or folder
            """
        self.idname.pop(objid)
        self.idtype.pop(objid)
        self.idparent.pop(objid) 
        self.idbyte.pop(objid)
        self.namedeductid(objid, objname)

    def rename_items_single(self, **kwargs):
        """The function 'deduct_items_single' will deduct items from idname, idtype, idparent, idtype & nameids. 
            It is expected to be called 
            3. renamed a folder
            kwargs = {"id":did,"oname":oldobjname,"nname":nfn}
            """
        id = kwargs['id']
        oname = kwargs['oname']
        nname = kwargs['nname']
        self.idname[id] = nname  
        Logger.log(f"rename_items_single to call nameaddid:id:{id} name:{nname}")    
        self.nameaddid(id, nname)
        
        Logger.log(f"rename_items_single to call namedeductid:id:{id} name:{oname}")
        self.namedeductid(id, oname)

    def nameaddid(self,id, name):
        """ The function 'nameaddid' is to update the self.nameids that is a list holds the relation of name and its ids (allows multiple ids for a name).
            A name is expected to be unique under a defined corpus.
            Thus the logic will firstly check if exist the record of the relation of the object name and id.
            Secondly, if it has the record, it will check if the object id has been in the list. If not, it will add a new element into the list. """
        if name in self.nameids:
            if  id not in self.nameids[name]:
                self.nameids[name].append(id)
        else:
            self.nameids[name] = [id]

    def namedeductid(self,id, oname):
        """ The function 'namedeductid' is to update the self.nameids that is a list holds the relation of name and its ids (allows multiple ids for a name).
            A name is expected to be unique under a defined corpus.
            When an id is deletd, it should also be deducted from the list of its name."""
        if self.get_id_byname(oname) is not None and id in self.get_id_byname(oname):
            self.nameids[oname].remove(id)
            Logger.log(f"namedeductid:id:{id} is removed from name:{oname}")
        else:
            Logger.log(f"namedeductid:id:{id} is not removed from name:{oname} caused not exist") 
    
    def nameidshowdetail(self, name):
        """case when a name with multiple ids, the helper function shows the detail to speify the id would like to anchor+"""
        elems = []
        for id in self.nameids[name]:
            elem = {'id':id,'name':self.idname[id],'parentName':self.idname[self.idparent[id]],'parentId':self.idparent[id],'byte':self.idbyte[id]}
            elems.append(elem)
        return elems
    
    def get_node_items(self):
        "node id is the root of the datastudio"
        nodeid = self._nodeid
        if nodeid is not None:
            resp = self.get_items(nodeid)
        
        if resp.status_code == 200:
            Logger.log(f"Request get_node_items from {self._get_items_url} with retrun code {resp.status_code} / get_items {resp.text}")  
        else:
            Logger.log(f"Request get_node_items from {self._get_items_url} with retrun code {resp.status_code} / fail on get_items {resp.text}") 

        return resp
    
    def set_node_items_all(self):
        "node id is the root of the datastudio"
        nodeid = self._nodeid
        if nodeid is not None:
            return self.set_items_all_by_tree(nodeid)

    def set_client_items_all(self,clientid):
        "Only specified client id info is showed under the root of the datastudio"
        resp = self.create_clientds_ifnot_exist(clientid)
        if resp['code'] != 3: nodeid = resp['info']['id']
        else: return resp

        if nodeid is not None:
            return self.set_items_all_by_tree(nodeid)
    
    def create_clientds_ifnot_exist(self, clientid):
        """"
        return code 1 : folder exist return id
                    2 : Create a new folder and return id
                    3 : Unexpecetd error
        Please Note that: the client data store will alwayse be created under the root
        """
        r = self.get_node_items()
        clientinfo = {}
        rc = {1:'folder exist return id',2:'Create a new folder and return id',3:'Unexpecetd error'}
        for elem in r.json():
            if elem['name'] == clientid and elem['type'] == 'D':
                clientinfo['name'] = clientid
                clientinfo['id'] = elem['id']
                code = 1

        if  len(clientinfo) == 0: 
            resp = self.add_folder(self._nodeid,clientid)
            if resp.status_code == 200:
                clientinfo['name'] = clientid
                clientinfo['id'] = resp.json()
                code = 2
            else: return {'code':3,"message":resp}

        if len(clientinfo) >= 0: self.cds = clientinfo
        return {'code':code,'info':clientinfo}


    def get_config_level1_items(self,level1nn):
        """"""
        objid = self._level1[level1nn]
        if objid is not None:
            resp = self.get_items(objid)
        
        if resp.status_code == 200:
            Logger.log(f"Request get_config_level1_items from {self._get_items_url} with retrun code {resp.status_code} / get_items {resp.text}")  
        else:
            Logger.log(f"Request get_config_level1_items from {self._get_items_url} with retrun code {resp.status_code} / fail on get_items {resp.text}") 

        return resp

    def get_name_byid(self, id:str)->list:
        """"""
        if id in self.idname:
            return self.idname[id]
        else:
            return {f'query objid {id} is not found!'}

    def get_byte_byid(self, id:str)->str:
        """"""
        if id in self.idbyte:
            return self.idbyte[id]
        else:
            return None

    def get_parent_byid(self, id:str)->str:
        """"""
        if id in self.idparent:
            return self.idparent[id]
        else:
            return None

    def get_type_byid(self, id:str)->str:
        """"""
        if id in self.idtype:
            return self.idtype[id]
        else:
            return None

    def get_path_byid(self, id:str)->str:
        """"""
        return self.make_path(id)

    def get_id_byname(self, name:str)->list:
        """"""
        if name in self.nameids:
            return self.nameids[name]
        else:
            return None

    def get_idd_byname(self, name):
        """"""
        if name in self.nameidshowdetail:
            return self.nameidshowdetail[name]
        else:
            return {}

    def get_downloadfileurl(self,fileid, valapikey=True):
        """  """
        if valapikey: self.val_apikey()   # Validate an API Key
        if self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return None

        payload = {"FileID":fileid}
        headers = {"ticket": self.apikey}
        resp = InnoDrive.irequests.post(self._get_download_file_url,json=payload, headers=headers)
        if resp.status_code == 200:
            Logger.log(f"Request get_downloadfileurl fileid: {fileid} from {self._get_download_file_url} with retrun code {resp.status_code} / get_items {resp.text}")  
            return resp.text.strip('"')

        else:
            Logger.log(f"Request get_downloadfileurl fileid: {fileid} from {self._get_download_file_url} with retrun code {resp.status_code} / fail on get_items {resp.text}") 
            return resp.text

    def get_downloadfile(self,fileid):
        url = self.get_downloadfileurl(fileid)
        resp_file = InnoDrive.irequests.get(url)
        return resp_file
   
    def upload_file(self, sfilename, sfilepath, folderid,  tfilename=None, overwrite='true', valapikey=True):
        """  """
        if valapikey: self.val_apikey()   # Validate an API Key
        if self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return {"status":"fail","msg":f"Have not the validate API Key to proceed!"}

        if tfilename == None: tfilename = sfilename
        files = [(tfilename,(sfilename,open(sfilepath,'rb')))]
        kwargs = {'parentId':folderid,'overwrite':overwrite}
        headers = {"ticket": self.apikey}
        resp = InnoDrive.irequests.post(self._upload_files_url, data=kwargs, files=files, headers=headers)
        
        if resp.status_code == 200:
            objid = resp.json()[0]['id']
            self.add_items_2levels(folderid, objid)   # the items_single relation  must be rest
            Logger.log(f"Request upload_file from {self._upload_files_url} for file name: {tfilename} with retrun code {resp.status_code} / get_items {resp.text}")  
            return {"status":"sucess","msg":resp}

        else:
            Logger.log(f"Request upload_file from {self._upload_files_url} for file name: {tfilename} with retrun code {resp.status_code} / fail on get_items {resp.text}") 
            return {"status":"fail","msg":resp}

    def add_folder(self, pfolderid, foldern, valapikey=True):
        """  """
        if valapikey: self.val_apikey()   # Validate an API Key
        if self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return None

        kwargs = {'parentId':pfolderid,'FolderName':foldern}
        headers = {"ticket": self.apikey}
        resp = InnoDrive.irequests.post(self._add_folder_url, json=kwargs, headers=headers)
        
        if resp.status_code == 200:
            objid = resp.json()
            self.add_items_2levels(pfolderid, objid)   # the items_single relation  must be rest            
            Logger.log(f"Request add_folder from {self._add_folder_url} with retrun code {resp.status_code}")  
            return resp

        else:
            Logger.log(f"Request add_folder from {self._add_folder_url} with retrun code {resp.status_code} ") 
            return resp
        
    def del_foldervfile(self, did, valapikey=True):
        """  """
        if valapikey: self.val_apikey()   # Validate an API Key
        if self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return {"status":"FAIL","errmsg":"Have not the validate API Key to proceed!"}

        if did == self._nodeid:
            Logger.log(f"Not allowd to del the node id")
            return {"status":"FAIL","errmsg":"Not allowed to del the node id"}


        kwargs = {'fileID':did}
        headers = {"ticket": self.apikey}
        objname = self.get_name_byid(did)
        resp = InnoDrive.irequests.post(self._delete_file_url, json=kwargs, headers=headers)
        
        if resp.status_code == 200:
            self.deduct_items_single(did,objname) 
            Logger.log(f"Request del_foldervfile objid {did} objname {objname} from {self._delete_file_url} with retrun code {resp.status_code}")  
            return resp

        else:
            Logger.log(f"Request del_foldervfile objid {did} objname {objname} from {self._delete_file_url} with retrun code {resp.status_code} ") 
            return resp

    def del_folder(self, did, valapikey=True):
        return self.del_foldervfile(did, valapikey)    

    def del_file(self, did, valapikey=True):
        return self.del_foldervfile(did, valapikey)     

    def rename_foldervfile(self, did, nfn, valapikey=True):
        """  """
        if valapikey: self.val_apikey()   # Validate an API Key
        if self.apikey == None: 
            Logger.log(f"Have not the validate API Key to proceed!")
            return None

        kwargs = {'fileID':did, 'FileName':nfn}
        headers = {"ticket": self.apikey}
        oldobjname = self.get_name_byid(did)
        resp = InnoDrive.irequests.post(self._rename_url, json=kwargs, headers=headers)
        
        if resp.status_code == 204:
            Logger.log(f"Request rename_foldervfile from {self._rename_url} with retrun code {resp.status_code} for id:{did},oldobjname:{oldobjname},newfilename{nfn}")
            self.rename_items_single(id=did, oname=oldobjname, nname=nfn)
            return resp

        else:
            Logger.log(f"Request del_foldervfile from {self._rename_url} with retrun code {resp.status_code} ") 
            return resp

    def rename_folder(self, did, nfn, valapikey=True):
        return self.rename_foldervfile(did, nfn, valapikey)

    def rename_file(self, did, nfn, valapikey=True):
        return self.rename_foldervfile(did, nfn, valapikey)

    def identity_check_by_hash(self,objids:list):
        """verify if input objids exists same identities by hashing value
        For simplicity, the file type is expecetd to be json
        If not the json type, it will return error"""
        hashtable = {}
        for objid in objids:
            getfile_r = self.get_downloadfile(objid)
            if getfile_r.status_code ==  200:
                file = getfile_r.text
            else:
                file = ""
            hashtable[objid] = hash(file)

        Logger.log(f"Hash table for {objids}: {hashtable}")
        
        flip = {}
        for key, value in hashtable.items():
            if value not in flip:
                flip[value] = [key]
            else:
                flip[value].append(key)

        Logger.log(f"Hash table for flip : {flip}")
        return flip

    def make_path(self,objid):
        """"A given file with objid, trace upstream to construc the full path"""
        initid = objid
        path = '/'+self.get_name_byid(initid)
        parent_id = self.get_parent_byid(initid)
        while not (parent_id == self._nodeid):
            parent_name = self.get_name_byid(parent_id)
            path = "/" + parent_name + path
            objid = parent_id
            parent_id = self.get_parent_byid(objid)

        self.idpath[initid] = path
        return path


    def path_maker(self,interceptid, filepath, resetinfo=False):

        """Given the intercept id (interceptid) and the file path (filepath), trace downstream from 
        the intercept id. The filepath should be represented like '/a/b/c/d/e'
        1. existed path is fully matched, the returning value should be the id of the 'e'.
        2. there is not any matched part, a path should be created
        3. partially matched, such as mathed '/a/b/c' it will create the right hand remained unmatched part
        """

        if type(filepath) is not str: return {"status":"error", "message": "given para:filepath is not a string type"}
        else: givenpath = filepath.strip('/').split('/')

        if resetinfo: self.set_items_all_by_tree(interceptid)
        m = 0  # m is the match indic
        n = len(givenpath)  # n is the number of th given path
        i = 0
        parentid = interceptid

        while i < n:

            if parentid in self.iditemsname: 
                names = self.iditemsname[parentid]
                # print(f"Names:{names}")
            else:
                names = [] 

            if givenpath[i] in names:
                matchid = self.get_id_byname_and_parentid(givenpath[i],parentid)
                if matchid["status"] == "OK":
                    parentid = matchid["objid"]
                    # print(f"Existed:parentid {parentid}, givenpath {givenpath[i]}")
                    i += 1
                else:
                    return {"status":"Error", "errmsg":f"Objname {givenpath[i]} found in folder id {parentid} but has not the Objid"}
            else:
                print(f"New: parentid {parentid}, givenpath {givenpath[i]}")
                resp = self.add_folder(parentid, givenpath[i])
                if resp.status_code == 200:
                    parentid = resp.json()
                    i += 1
                else:
                    return {"status":"Error", "errormdg":f"{resp.text}"}

        endpointid = parentid

        return {"status":"OK", "endpoint":endpointid}

    def get_id_byname_and_parentid(self, objname,parentid,resetinfo=False):
        """The function will accept the given objname (file or folder) and its parent id and return the id of the object name
            Generally, a name is not allowed to be duplicated belong to the same parent folder. Thus, it will alwayse return a unique and only 
            one objectid if the name is in the parent.
        """
        # print(f"objname{objname}:paprentid{parentid}")
        if resetinfo: self.set_items_all_by_tree(parentid)
        if objname in self.iditemsname[parentid]:
            for id in self.iditemsid[parentid]:
                if self.idname[id] == objname:
                    objid = id
                    return {"status":"OK", "objid":objid}
        else:
            return {"status":"Not found", "msg":f"Obj name {objname} is not in parent id {parentid}"}

    def files_similarity_inorder_lines(self, basefile:list, targetfile:list):
        """The function is used when interesting points are on the similarity (measured by percentage) of two files. it will
        read line by line in order 
        Please noted that: The file format is restricetd by list type"""
        return FilesCompare(basefile, targetfile, "inorder", "text")

    def files_similarity_unorder_lines(self, basefile:list, targetfile:list):
        """The function is used when interesting points are on the similarity (measured by percentage) of two files. it will
        read line by line in basefile and each single line is compared for all lines in targetFiles. Means that it will not consider the order of lines.
        """
        return FilesCompare(basefile, targetfile, "unorder", "text")

    def files_compare(self,basefileid, targetfileid, category):
        """Function to compare two files by given ids.
        The category is to seperate inorder or unorder"""

        basefile_r = self.get_downloadfile(basefileid)
        targetfile_r = self.get_downloadfile(targetfileid)
        if basefile_r.json()['status'] == "success":
            basefile = basefile_r.json()['result']
            if targetfile_r.json()['status'] == "success":
                targetfile = targetfile_r.json()['result']
                if category == "inorder":
                    return self.files_similarity_inorder_lines(basefile, targetfile)
                if category == "unorder":
                    return self.files_similarity_unorder_lines(basefile, targetfile)
            else:
                Logger.log(f"Request for downloading file (fileid: {targetfileid} is not sucess")
        else:
            Logger.log(f"Request for downloading file (fileid: {basefileid} is not sucess")

class FilesCompare():

    category = ""
    files = {}

    def __init__(self, basefile, targetfile, category, type="text"):
        if category == "inorder":
            self.category = "inorder"
            self.files_similarity_inorder_lines(basefile, targetfile)
        
        if category == "unorder":
            self.category = "unorder"
            self.files_similarity_unorder_lines(basefile, targetfile)

    def files_similarity_inorder_lines(self, basefile:list, targetfile:list):
        """The function is used when interesting points are on the similarity (measured by percentage) of two files. it will
        read line by line in order 
        Please noted that: The file format is restricetd by list type"""
        self.linenb = len(basefile)
        self.linent = len(targetfile)

        iden_count = 0
        diff_count = 0
        iden_content = {}
        diff_content = {}

        for nlineb in range(self.linenb):
            if nlineb < self.linent:     
                
                if basefile[nlineb] == targetfile[nlineb]:
                    iden_count += 1
                    iden_content['line:'+ str(nlineb)] = [basefile[nlineb]]
                else:
                    diff_count += 1
                    diff_content['basefile line:'+str(nlineb)] = [basefile[nlineb]]
                    diff_content['targetfile line:'+str(nlineb)] = [targetfile[nlineb]]
            else:   # Case when the base files has line number which is greater than target file
                diff_count += 1
                diff_content['basefile line'+str(nlineb)] = [basefile[nlineb]]
        
        if (nlineb-self.linent) < 0:   # Case when the target files has line number which is greater than base file
            for extra in range(nlineb+1,self.linent):
                diff_count += 1
                diff_content['targetfile:'+str(extra)] = [targetfile[extra]]

        self.files["basefile"] = [basefile]
        self.files["targetfile"] = [targetfile]
        self.iden_count = iden_count
        self.iden_content = iden_content
        self.diff_count = diff_count
        self.diff_content = diff_content
        self.simi_rate = iden_count/(iden_count+diff_count)

    def files_similarity_unorder_lines(self, basefile:list, targetfile:list):
        """The function is used when interesting points are on the similarity (measured by percentage) of two files. it will
        read line by line in basefile and each single line is compared for all lines in targetFiles. Means that it will not consider the order of lines.
        The concept is quite different with inorder compare.
        If the similar rate is 1.0, it will mean the base file is included or equal the target file 
        """
        self.linenb = len(basefile)
        self.linent = len(targetfile)

        iden_count = 0
        diff_count = 0
        iden_content = {}
        diff_content = {}

        for nlineb in range(self.linenb):
            lnbt = 0 # Same count for a single line 
            for nlinet in range(self.linent):
                if basefile[nlineb] == targetfile[nlinet]:
                    iden_count += 1
                    lnbt += 1
                    iden_content['basefile line:'+str(nlineb)] = [basefile[nlineb]]
                    iden_content['targetfile line:'+str(nlinet)] = [targetfile[nlinet]]
            
            if lnbt == 0:
                diff_count += 1
                diff_content['basefile line:'+str(nlineb)] = [basefile[nlineb]]
                Logger.log(f"file similarity unorder compare found line number {nlineb} in basefile has not the same for all lines in target file")

        self.files["basefile"] = [basefile]
        self.files["targetfile"] = [targetfile]
        self.iden_count = iden_count
        self.iden_content = iden_content
        self.diff_count = diff_count
        self.diff_content = diff_content
        self.simi_rate = iden_count/(iden_count+diff_count)