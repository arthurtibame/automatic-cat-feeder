from utils.google_api import Gsheet, GoogleApi
import settings

data = GoogleApi(23).to_list()

gs = Gsheet(settings.GOOGLE_SHEET_KEY)
gs.create_connection()

gs.insert_rows([data])



