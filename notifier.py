#write messages on google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import streamlit as st

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GSHEET_CREDS_JSON"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("AI Assignment Submissions").sheet1

def log_submission(student_email, assignment, score, feedback, url):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, student_email, assignment, str(score), feedback, url])


