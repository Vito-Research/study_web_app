

import pandas as pd
import gspread
import df2gspread as d2g
import uuid

def uploadFile(df):

    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'jsonFileFromGoogle.json', scope)
        
    gc = gspread.authorize(credentials)
    spreadsheet_key = 'red_url_code_goes_here'
    wks_name = 'Master'
    d2g.upload(df, spreadsheet_key, wks_name, credentials=credentials, row_names=True)









