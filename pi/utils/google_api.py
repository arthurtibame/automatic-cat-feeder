from datetime import datetime
from socket import gethostname
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import settings

class GoogleApi(object):
    def __init__(self, weight, data_type="add_cat_feed") -> None:
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")        
        # google sheet column here 
        self.hostname=gethostname()
        self.data_type=data_type        
        self.weight=weight
        self.createtime=now
        self.modifytime=now  


    def to_dict(self) -> dict:
        data = {
            "machine": self.hostname,
            "data_type": self.data_type,
            "data":[
                {                    
                    "weight": self.weight,
                    "createtime": self.createtime,
                    "modifytime": self.modifytime
                }
            ]    
        }
        return data

    def to_list(self) -> list:
        return [self.hostname, self.data_type, self.weight, self.createtime, self.modifytime]


class Gsheet:    
    __credentials = None
    def __init__(self, key) -> None:        
        self.key = key
        self.sheet = None
        self.col_name=None
        self.client = None
        __scopes = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_name(
           settings.GOOGLE_SECRET_PATH, __scopes)                 
    
    def create_connection(self) -> None:                
        self.client = gspread.authorize(self.__credentials)        
        self.sheet = self.client.open_by_key(self.key)

    def insert_rows(self, values, worksheet="Bear", row=2, value_input_option='RAW'):
        """[summary]

        Args:
            values ([list]): [description] list of values to insert 
            worksheet (str, optional): [description]. Defaults to "work1".
            row (int, optional): [description]. Defaults to 2.
            value_input_option (str, optional): [description]. Defaults to 'RAW'.
        """
        self.sheet.worksheet(worksheet).insert_rows(values=values, value_input_option=value_input_option, row=row)

    def row_count(self, worksheet="work1"):
        self.sheet.worksheet(worksheet).row_count


    def get_all_values(self, worksheet) -> list:
        _ = self.sheet.worksheet(worksheet).get_all_values()     
        self.col_name= _[0]
        return _[1:]
