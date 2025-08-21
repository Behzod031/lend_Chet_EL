from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

app = Flask(__name__)

# Путь к credentials.json (лежит рядом с app.py)
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "credentials.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Авторизация Google Sheets
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Открываем таблицу и нужный лист
spreadsheet = client.open("Xonsaroy_Online_Chat")
worksheet = spreadsheet.worksheet("Efir")


# Главная страница (форма)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        city = request.form.get('city')
        date = datetime.now().strftime('%Y-%m-%d')

        # Сохраняем данные в Google Sheets
        worksheet.append_row([name, phone, city, date])

        # Редиректим на отдельный роут /telegram
        return redirect(url_for('telegram'))

    return render_template('index.html')


# Страница Telegram (доступна напрямую по /telegram)
@app.route('/telegram')
def telegram():
    return render_template('telegram.html', utm="ads")


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=1232)
