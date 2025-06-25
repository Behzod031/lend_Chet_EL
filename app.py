import os
from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Путь к JSON-файлу с ключами: из переменной окружения или по умолчанию рядом с app.py
SERVICE_ACCOUNT_FILE = os.environ.get(
    "GOOGLE_CREDENTIALS_PATH",
    os.path.join(os.path.dirname(__file__), "credentials.json")
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Авторизация в Google Sheets
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Открываем таблицу и лист
spreadsheet = client.open("Chet-el mijozlar")
worksheet = spreadsheet.worksheet("MyLandingDB")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        country = request.form.get('country')

        # Записываем данные в таблицу
        worksheet.append_row([name, phone, country])

        # Рендерим страницу с переходом в Telegram
        return render_template('telegram.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 1232)), debug=False)
