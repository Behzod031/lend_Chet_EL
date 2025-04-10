from flask import Flask, render_template, request
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Указываем путь к вашему JSON-файлу с ключами
SERVICE_ACCOUNT_FILE = r"C:\Users\XS-NB-OP\PycharmProjects\call_center - marketing_bot\credentials.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Открываем таблицу "Chet-el mijozlar" и выбираем вкладку "MyLandingDB"
spreadsheet = client.open("Chet-el mijozlar")
worksheet = spreadsheet.worksheet("MyLandingDB")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        country = request.form.get('country')

        # Добавляем новую строку с данными в Google Sheets
        worksheet.append_row([name, phone, country])

        # Показываем страницу с сообщением об успешной отправке
        return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=1232)

