from flask import Flask, request, render_template, jsonify
from datetime import datetime
import re
import webbrowser

app = Flask(__name__)

surname_scr = ""
name_scr = ""
name_surname_err = "<span>Поля должны содержать только символы русского алфавита без пробелов, спецсимволов и цифр</span>"
birth_error = "Вы должны быть не моложе 18 лет для завершения регистрации. Пожалуйста, проверьте введенную дату рождения"
null_birth_error = "Поле с датой не заполнено"
email_error = "Введите корректную электронную почту"
null_email_error = "Поле с электронной почтой не заполнено"
scr_disp = "<script>changeClassProperty();</script>"
scr_hide = "<script>changeClassPropertyHide();</script>"


li_amount = 10 # визуальная составляющая, количество квадратов на фоне
today_str = datetime.today().strftime('%Y-%m-%d')

@app.route('/')
def index():
    return render_template('register.html', max_date=today_str, li_amount='<li></li>\n'*li_amount)
    
@app.route('/validate_surname', methods=['POST'])
def validate_surname():
    surname = request.form.get('surname')
    name = request.form.get('name')
    if surname is None or not normal(surname):
        # print(surname, normal(surname))
        surname_scr = scr_input_form("surname", "red")
        return surname_scr + name_scr + spanned(name_surname_err)
    surname_scr = scr_input_form("surname", "#1891ac")
    if normal(surname) and normal(name):
        return surname_scr + name_scr
    return surname_scr + name_scr + spanned(name_surname_err)

@app.route('/validate_name', methods=['POST'])
def validate_name():
    surname = request.form.get('surname')
    name = request.form.get('name')
    if name is None or not normal(name):
        # print(name, normal(name))
        name_scr = scr_input_form("name", "red")
        return surname_scr + name_scr + name_surname_err
    name_scr = scr_input_form("name", "#1891ac")
    if normal(surname) and normal(name):
        return surname_scr + name_scr
    return surname_scr + name_scr + name_surname_err

@app.route('/validate_birthdate', methods=['POST'])
def validate_birthdate():
    date = request.form.get('birth-date')
    today = datetime.today()
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
        age = (today - date).days // 365
        if age < 18:
            return scr_input_form("birth-date", "red") + birth_error
        else:
            return scr_input_form("birth-date", "#1891ac")
    else: return scr_input_form("birth-date", "red") + null_birth_error

@app.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form.get('email')
    print(email)
    if not re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,6}$', email):
        if email is None or email == '': return scr_input_form("email", "red") + null_email_error
        return scr_input_form("email", "red") + email_error
    else: return scr_input_form("email", "#1891ac")
    
@app.route('/validation-messages', methods=['POST'])
def validation_messages():
    return scr_disp
    
@app.route('/hide-messages', methods=['POST'])
def hide_messages():
    return scr_hide
    
# функция для выбора параметров скрипта js
def scr_input_form(name, color):
    return f'<script>changeInputBorderColor("{name}", "{color}");</script>'
def spanned(str):
    return f"<span id=\"displaying\">{str}</span>"
# функция для проверки имени или фамилии
def normal(str):
    if not re.match("^[А-Яа-я]+$", f"{str}"): return False
    return True

if __name__ == "__main__":
    # webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
    
    