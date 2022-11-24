import re
from tools.logger import Logger


def get_measure_column(measure_type):
    if measure_type == 0:
        return "CASE \n\t\t\t\tWHEN SPC_CHART_TYPE_CD LIKE 'AG%' THEN AVG_MEAS \n\t\t\t\tWHEN SPC_CHART_TYPE_CD LIKE '%X%' THEN X_MEAS \n\t\t   END"

    measure_type_code_list = ['DEFAULT', 'AVG', 'RNG', 'SDEV', 'UNF1', 'UNF2', 'MAX', 'MIN', 'X', 'RM']
    code = measure_type_code_list[measure_type]
    return f'{code}_MEAS'


def get_item_columns(operation, equipment, edc_items, prfx_opra_eqpt=True):
    if not edc_items: return '', ''

    item_select_fmt = '"D"."{0}" AS "{1}_{2}_{0}"' if prfx_opra_eqpt else '"D"."{0}" AS "{0}"'
    item_select = ','.join([item_select_fmt.format(item, operation, equipment) for item in edc_items])
    item_column = ','.join([f'"D"."{item}" VARCHAR' for item in edc_items])
    item_select = ',\n\t\t\t' + item_select
    item_column = f'({item_column})'
    return item_select, item_column


class SqlBuffer:

    def __init__(self, sql, conj='WHERE', alias=''):
        self._sql = sql
        self._conj = conj

        if alias and not alias.endswith('.'): alias += '.'
        self._alias = alias


    def alias(self, alias):
        if alias and not alias.endswith('.'): alias += '.'
        self._alias = alias

        return self


    def append_sql(self, appended):
        self._sql += f'\n\t{appended}'


    def append_where(self, appended):
        self._sql += f'\n\t{self._conj:>6} {appended}'
        if self._conj == "WHERE": self._conj = "AND"


    def add_date(self, column, date_start, date_end, ignore_time=False):
        if len(date_start) == 7: date_start += "-01"
        if len(date_end) == 7: date_end += "-01"

        time_start = "" if ignore_time else "00:00:00"
        time_end = "" if ignore_time else "23:59:59"
        
        self.append_where(f"{self._alias}{column} BETWEEN TO_TIMESTAMP('{date_start} {time_start}', 'yyyy-MM-dd HH:mm:ss', 'GMT+8') AND TO_TIMESTAMP('{date_end} {time_end}', 'yyyy-MM-dd HH:mm:ss', 'GMT+8')")

        return self


    def add(self, column, value):
        if value != "*": self.append_where(f"{self._alias}{column} = '{value}'")

        return self


    def add_in(self, column, values):
        if values and len(values) > 0 and '*' not in values:
            quoted = ','.join(f"'{v}'" for v in values)
            self.append_where(f"{self._alias}{column} IN ({quoted})")
        
        return self


    def add_in_sub(self, column, sql):
        sql = sql.replace("\n", "\n\t\t")
        self.append_where(f"{self._alias}{column} IN ({sql}\n\t\t   )")

        return self


    def add_like(self, column, value, add_percent=True):
        percent_sign = '%' if add_percent else ''
        self.append_where(f"{self._alias}{column} LIKE '{value}{percent_sign}'")
        
        return self


    def add_not_null(self, column):
        self.append_where(f"{self._alias}{column} IS NOT NULL")

        return self


    def add_between_str(self, column, start, end):
        self.append_where(f"{self._alias}{column} BETWEEN '{start}' AND '{end}'")

        return self


    def order_by(self, column):
        self.append_sql(f" ORDER BY {self._alias}{column}")

        return self


    #c200117:ownerCode可以是"*"、"P"、"E"、"D"、"P+E"、"P+D"、"E+D"，或是直接單個或多個ownerCode，例如"AE02,RES0,QTAP"
    def check_owner_code(self, owner_code):
        if owner_code == "*": return self

        code_dict = {
            "P": ["AE01", "AE02", "AE03", "AE04", "AE05", "AE06", "AE07", "AE08", "AE09", "AE10", "CRN0", "LCDA", "LCDB", "PPLT", "PROD", "QTAP", "RES0", "RCS0", "TF01", "QRA0"],
            "E": ["EPLT", "ETCH", "INSP", "INT0", "PHOT", "PM00", "AMHS", "TEST", "RD00", "TF00"],
            "D": ["DUMY", "BARE"]
        }
            
        code = []
        if len(owner_code) < 4:
            keys = re.split('\\+| |,', owner_code)
            for key in keys:
                if key in code_dict:
                    code.extend(code_dict[key])
        else:
            code = owner_code.split(',')

        return self.add_in("OWNER_CD", code)


    #c191203:依據輸入的逗號分隔字串，"03,08,05,02"，產生filter字串，"_YY_Y__Y"
    def check_chamber_code(self, chamber_code):
        if chamber_code == "00" or chamber_code == "0" or chamber_code == "*": return self

        try:
            code_arr = chamber_code.split(',') #["03","08","05","02"]
            int_arr = [int(code) for code in code_arr] #[3,8,5,2]

            #產生n個字元，n為int_arr裡最大者，i=1~n，如果i在int_arr裡，第i個字元為"Y"，否則為"_"
            #例如n=8, i=2,3,5,8為"Y"，其餘為"_"，["_","Y","Y","_","Y","_","_","Y"]
            filter_arr = ['Y' if i in int_arr else '_' for i in range(1, max(int_arr)+1)]
            filter = ''.join(filter_arr) #"_YY_Y__Y"
            if len(filter) > 0:
                return self.add_like("CHMBR_TXT", filter)

        except Exception as err:
            logger = Logger.default()
            logger.error(f'"{err.args[0]}" on check_chamber_code() in sql_buffer.py chamber_code={chamber_code}')
        
        return self



    @property
    def sql(self):
        return self._sql