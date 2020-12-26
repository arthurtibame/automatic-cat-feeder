import requests
from datetime import datetime
from socket import gethostname
import settings

class GoogleApi(object):
    def __init__(self, cat_name, weight, data_type="add_cat_feed") -> None:
        now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.url=settings.GOOGLE_FORM_URL
        # google sheet column here 
        self.hostname=gethostname()
        self.data_type=data_type
        self.cat_name=cat_name
        self.weight=weight
        self.createtime=now
        self.modifytime=now

    def insert(self):
        data = {
            "machine": self.hostname,
            "data_type": self.data_type,
            "data":[
                {
                    "cat_name": self.cat_name,
                    "weight": self.weight,
                    "createtime": self.createtime,
                    "modifytime": self.modifytime
                }
            ]    
        }
        res = requests.post(self.url, data=data)
    
