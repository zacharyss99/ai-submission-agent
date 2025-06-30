#write messages on google sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("AI Assignment Submissions").sheet1

def log_submission(student_email, assignment, score, feedback, url):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([now, student_email, assignment, str(score), feedback, url])
    

