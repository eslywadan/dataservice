from pickle import FALSE, TRUE
from random import randint
from time import sleep
import pytest
from  tools.sec_loader import SecretLoader
from tools.config_loader import ConfigLoader
from tools.innodrive import InnoDrive
from tools.logger import Logger
import time, os, io, json

class TestInoDrv():
    inodrv = InnoDrive()
    def test_api_ticket(cls):
        assert cls.inodrv.apikey is not None

    def test_val_apikey(cls):
        ckey = cls.inodrv.apikey
        cls.inodrv.val_apikey()
        vkey = cls.inodrv.apikey
        assert ckey == vkey
        
        original_apikey_dur = cls.inodrv._apikey_dur
        cls.inodrv._apikey_dur = 1
        time.sleep(3)
        cls.inodrv.val_apikey()
        newkey = cls.inodrv.apikey
        cls.inodrv._apikey_dur = ConfigLoader.config("innodrive")["apikey_dur"]
        assert vkey != newkey
        cls.inodrv._apikey_dur = original_apikey_dur

    def get_item(cls):
        resp1 = cls.inodrv.get_items("APDRV_DATASTUDIO")
        resp2 = cls.inodrv.get_node_items()
        assert resp1.json() == resp2.json()

    def test_upload_file_same_fname(cls):
        sfilen = "source_api_edc_raw.json"
        sfilep = os.path.join("data/eng_test_data",sfilen)
        folderid = ConfigLoader.config("innodrive")["nodeid"]
        resp = cls.inodrv.upload_file(sfilen, sfilep,folderid) 
        assert resp["msg"].status_code == 200

    def test_upload_file_diff_fname(cls):
        sfilen = "AIDeveloper.png"
        tfilen = "Superman.png"
        sfilep = os.path.join("data",sfilen)
        folderid = ConfigLoader.config("innodrive")["nodeid"]
        resp = cls.inodrv.upload_file(sfilen, sfilep,folderid,tfilen) 
        assert resp["msg"].status_code == 200

    def test_get_file(cls):
        gres = cls.inodrv.get_id_byname_and_parentid("AIDeveloper.png",cls.inodrv._nodeid)
        if gres["status"]=="OK": fileid = gres["objid"] 
        resp = cls.inodrv.get_downloadfile(fileid)
        assert resp.content is not None


    def test_add_del_folder(cls):
        foldername = "NewFolderTest"
        if cls.inodrv.get_id_byname(foldername) is not None:
            objid = cls.inodrv.get_id_byname(foldername)[0]
            r = cls.inodrv.del_folder(objid)
            if r.status_code != 200:print(f"status code: {r.status_code}, message:{r.text}")
            assert r.status_code == 200

        pfolderid = ConfigLoader.config("innodrive")["nodeid"]
        resp = cls.inodrv.add_folder(pfolderid,foldername) 
        if resp.status_code != 200:print(f"status code: {resp.status_code}, message:{resp.text}")
        assert resp.status_code == 200

        objids = cls.inodrv.get_id_byname(foldername)
        assert  objids is not None
        objid = objids[0]
        r = cls.inodrv.del_folder(objid)
        if r.status_code != 200:print(f"status code: {r.status_code}, message:{r.text}")
        assert r.status_code == 200

        objids = cls.inodrv.get_id_byname(foldername)
        
        assert len(objids) == 0


    def test_rename_folder(cls):
        """The test case will create a folder 'RenameFolderTest' and then rename it.
            The id should be renmained but the attribute of name should be changed.
            Thus the asserting will check the correctness of get_name_byid """
        foldername = "RenameFolderTest"
        newfoldername = "RenameFolderTest-NewName"

        if cls.inodrv.get_id_byname(foldername) is not None:
            objid = cls.inodrv.get_id_byname(foldername)[0]
            r = cls.inodrv.del_folder(objid)
            if r.status_code != 200:print(f"status code: {r.status_code}, message:{r.text}")
            assert r.status_code == 200

        if cls.inodrv.get_id_byname(newfoldername) is not None:
            objid = cls.inodrv.get_id_byname(newfoldername)[0]
            r = cls.inodrv.del_folder(objid)
            assert r.status_code == 200

        pfolderid = ConfigLoader.config("innodrive")["nodeid"]
        resp = cls.inodrv.add_folder(pfolderid,foldername) 
        assert resp.status_code == 200

        objid = cls.inodrv.get_id_byname(foldername)[0] 
        assert  objid is not None
        
        Logger.log(f"Tests:test reanme folder name: oldfolder name:{foldername}:New folder name:{newfoldername} ")
        r = cls.inodrv.rename_folder(objid, newfoldername)
        assert r.status_code == 204
        
        objids = cls.inodrv.get_id_byname(newfoldername)
        objid = objids[0]
        assert objid not in cls.inodrv.get_id_byname(foldername)
        assert cls.inodrv.nameids[newfoldername] is not None
        assert objids == cls.inodrv.get_id_byname(newfoldername)
        assert cls.inodrv.get_name_byid(objid) == newfoldername

    def test_files_identity(cls):
        test_file_name = 'source_api_edc_raw.json'
        objids = cls.inodrv.get_id_byname(test_file_name)
        Logger.log(f"{cls.inodrv.identity_check_by_hash(objids)}")

    def test_files_compare(cls):
        test_file_name = 'source_api_edc_raw.json'
        objids = cls.inodrv.get_id_byname(test_file_name)
        Logger.log(f"files_compare tests for {objids}")
        objsn = len(objids)
        
        for i in range(objsn-1):
            cp1 = cls.inodrv.files_compare(objids[i],objids[i+1],'inorder')
            cp2 = cls.inodrv.files_compare(objids[i],objids[i+1],'unorder')
            Logger.log(f"Inorder compare result: Identical Count:{cp1.iden_count} / Diff Count:{cp1.diff_count}")
            Logger.log(f"Unorder compare result: Identical Count: {cp2.iden_count} / Diff Count:{cp2.diff_count}")
            assert cp1.simi_rate == 1.0
            assert cp2.simi_rate == 1.0


def test_files_compare():
    tidv = FileCompareAux()
    test_file_name = 'source_api_edc_raw.json'
    idrv = TestInoDrv.inodrv
    objids = idrv.get_id_byname(test_file_name)
    tidv.objids = objids
    tidv.test_file_name = test_file_name
    tidv.mock_temp(1)
    aux_files_compare(tidv)

    tidv.mock_temp(2)
    aux_files_compare(tidv)

    tidv.mock_temp(3)
    aux_files_compare(tidv)


def aux_files_compare(tidv):
    tidv.read_temp()

    tidv.compare_temp_inorder()
    for key in tidv.compare_result_inorder.keys():
        cpri = tidv.compare_result_inorder[key]
        Logger.log(f"cpri.pair: {key} : identity count: {cpri.iden_count} : diff_content {cpri.diff_content} ")

    tidv.compare_temp_unorder()
    for key in tidv.compare_result_unorder.keys():
        cpru = tidv.compare_result_unorder[key]
        Logger.log(f"cpru.pair: {key} : identity count: {cpru.iden_count} : diff_content {cpru.diff_content} ")


class FileCompareAux:

    objids = []
    test_file_name = ""

    def __init__(self):
        self.temppath = 'temp'

    def mock_temp(self, seasoning_data=0):

        """"The function will retrieve the data from innodrive by given ids and do seasoning data.
        The seasoning type is seperated by number, thus it will allowed different seasoning flavors.
        seasoning type = 1 : Arbitarily select one file from ids and then alsp select arbitarily one line, The selected line is
        seasoned by replacing the text
        seasoning type = 2 : Dual selected lines are swapped the line location """

        arbitary_file = randint(0, len(self.objids))
        fn = 0
        for objid in self.objids:
            r = TestInoDrv.inodrv.get_downloadfile(objid)
            rf = r.text

            if fn == arbitary_file:
                srf = self.mock_data(seasoning_data, objid, rf)
            else:
                srf = rf

            filepath = os.path.join(self.temppath, objid + '.json')
            f = open(filepath, 'w')
            for ln in srf:
                f.write(str(ln)+"\n")
            f.close()
            fn += 1

    def mock_data(self, seasoning_data, objid, rf):
        arbitary_line1 = randint(0, len(rf)-1)
        if arbitary_line1 == len(rf)-2: arbitary_line1 = arbitary_line1-1
        arbitary_line2 = randint(arbitary_line1, len(rf)-2)
        Logger.log(f"file: {objid} is seasoned (type:{seasoning_data}) with arbitary_line1 {arbitary_line1} arbitary_line2 {arbitary_line2}")
            
        srf = []
        for lnn in range(len(rf)):
            ln = rf[lnn]
            if seasoning_data == 1 and arbitary_line1 == lnn:
                ln = "The line is seasoned for testing ^^"
                Logger.log(f"file: {objid} is seasoned (type:{seasoning_data}) by {ln} at line number {lnn}")
            
            if seasoning_data == 2 and (arbitary_line1 == lnn or arbitary_line2 == lnn):
                if arbitary_line1 == lnn:
                    ln = rf[arbitary_line2]
                if arbitary_line2 == lnn:
                    ln = rf[arbitary_line1]
                Logger.log(f"file: {objid} is seasoned (type:{seasoning_data}) by {ln} at line number {lnn}")
            
            if seasoning_data == 3 and (arbitary_line1 == lnn or arbitary_line2 == lnn):
                Logger.log(f"file: {objid} is seasoned (type:{seasoning_data}) by {ln} at line number {lnn}")
                continue
        
            srf.append(ln)
        return srf

    def read_temp(self):

        self.fr = {}
        for objid in self.objids:
            filepath = os.path.join(self.temppath, objid + '.json')
            f =  open(filepath, 'r')
            self.fr[objid] = f.readlines()

    def compare_temp_inorder(self):

        self.compare_result_inorder = {}
        for bobjid in self.objids:
            f1 = self.fr[bobjid]
            for tobjid in self.objids:
                if bobjid == tobjid:pass
                else:
                    f2 = self.fr[tobjid] 
                    self.compare_result_inorder[bobjid, tobjid] = TestInoDrv.inodrv.files_similarity_inorder_lines(f1, f2)


    def compare_temp_unorder(self):

        self.compare_result_unorder = {}
        for bobjid in self.objids:
            f1 = self.fr[bobjid]
            for tobjid in self.objids:
                if bobjid == tobjid:pass
                else:
                    f2 = self.fr[tobjid] 
                    self.compare_result_unorder[bobjid, tobjid] = TestInoDrv.inodrv.files_similarity_unorder_lines(f1, f2)


        

