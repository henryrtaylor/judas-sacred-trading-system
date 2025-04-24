import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Define the scope and credentials
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds_path = 'config/judas-sheets-creds.json'
sheet_id = '1zDmZPAX_dG_NjAHXNbN8n82EINJxzI9DQczBXZpVq2k'

creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Open the sheet by ID
sheet = client.open_by_key(sheet_id)
worksheet = sheet.get_worksheet(0)  # First tab

# Append a test log row
timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
row = [timestamp, "TEST_EVENT", "AAPL", "Success"]
worksheet.append_row(row)

print("✅ Row written to Google Sheet.")