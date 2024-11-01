from flask import Flask, request, render_template, jsonify
from datetime import datetime
import re
import webbrowser

app = Flask(__name__)
errors = {
    "birth":"Вы должны быть не моложе 18 лет для завершения регистрации. Пожалуйста, проверьте введенную дату рождения",
    "null_birth":"Поле с датой не заполнено",
    "email":"Введите корректную электронную почту",
    "null_email":"Поле с электронной почтой не заполнено",
    "name_surname":"Поля должны содержать только символы русского алфавита без пробелов, спецсимволов и цифр",
    "pass":"Допустимы только латинские символы, цифры и спецсимволы: @$!%*?&",
    "easy_pass":"Пароль слишком легкий. Должны быть хотя бы по одной: заглавная буква, строчная буква, цифра и спецсимвол",
    "short_pass":"Пароль слишком короткий",
    "null_pass":"Поле с паролем не заполнено",
    "pass_confirm":"Пароли не совпадают",
    "before_pass_confirm":"Сначала введите верный пароль выше"
}

confirmed_fields = {
    "surname":False,
    "name":False,
    "birth-date":False,
    "email":False,
    "password":False,
    "pass-confirm":False,
}

surname_scr = ""
name_scr = ""
scr_disp = "<script>changeClassProperty();</script>"
scr_hide = "<script>changeClassPropertyHide();</script>"
scr_enable = "<script>enableAllButtons();</script>"


li_amount = 10 # визуальная составляющая, количество квадратов на фоне
today_str = datetime.today().strftime('%Y-%m-%d')

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('register.html', max_date=today_str, li_amount='<li></li>\n'*li_amount)
    
@app.route('/validate_surname', methods=['POST'])
def validate_surname():
    confirmed_fields["surname"] = False
    surname = request.form.get('surname').strip()
    name = request.form.get('name').strip()
    if surname is None or not normal_str(surname):
        # print(surname, normal(surname))
        surname_scr = scr_input_form("surname", "red")
        return surname_scr + name_scr + spanned(errors["name_surname"])
    surname_scr = access_former("surname")
    if normal_str(surname) and normal_str(name):
        confirmed_fields["surname"] = True
        confirmed_fields["name"] = True
        return surname_scr + name_scr
    return surname_scr + name_scr + spanned(errors["name_surname"])

@app.route('/validate_name', methods=['POST'])
def validate_name():
    confirmed_fields["name"] = False
    surname = request.form.get('surname').strip()
    name = request.form.get('name').strip()
    if name is None or not normal_str(name):
        # print(name, normal(name))
        name_scr = scr_input_form("name", "red")
        return surname_scr + name_scr + spanned(errors["name_surname"])
    name_scr = access_former("name")
    if normal_str(surname) and normal_str(name):
        confirmed_fields["surname"] = True
        confirmed_fields["name"] = True
        return surname_scr + name_scr
    return surname_scr + name_scr + spanned(errors["name_surname"])

@app.route('/validate_birthdate', methods=['POST'])
def validate_birthdate():
    date = request.form.get('birth-date')
    if date:
        date = datetime.strptime(date, '%Y-%m-%d')
        age = (datetime.today() - date).days // 365
        if age < 18:
            return error_former("birth-date", errors["birth"])
        return access_former("birth-date")
    return error_former("birth-date", errors["null_birth"])

@app.route('/validate_email', methods=['POST'])
def validate_email():
    email = request.form.get('email').strip()
    print(email)
    if not normal_email(email):
        if email is None or email == '': return error_former("email", errors["null_email"])
        return error_former("email", errors["email"])
    return access_former("email")
    
@app.route('/validate_pass', methods=['POST'])
def validate_pass():
    password = request.form.get('password')
    if password == "":
        return error_former("password", errors["null_pass"])
    if not len(password) >= 8:
        return scr_input_form("password", "red") + spanned(errors["short_pass"])
    if not normal_pass(password):
        return error_former("password", errors["pass"])
    if not (re.search(r"\d", password) and re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password) and re.search(r"[@$!%*?&]", password)):
        return error_former("password", errors["easy_pass"])
    return access_former("password")

@app.route('/validate_pass_conf', methods=['POST'])
def validate_pass_conf():
    if not confirmed_fields["password"]:
        return error_former("pass-confirm", errors["before_pass_confirm"])
    passconf = request.form.get('pass-confirm')
    password = request.form.get('password')
    if not password == passconf:
        return error_former("pass-confirm", errors["pass_confirm"])
    return access_former("pass-confirm")
    
@app.route('/validation-messages', methods=['POST'])
def validation_messages():
    result = ""
    for key, value in confirmed_fields.items():
        if not value:
            result += error_former(key, error_name=None)
    if result == "":
        return ""
    print(result)
    return result + scr_disp
    
@app.route('/hide-messages', methods=['POST'])
def hide_messages():
    result = ""
    for key, value in confirmed_fields.items():
        if not value:
            result += error_former(key, error_name=None)
    if result == "":
        print("ВСЕ ОК")
        return scr_enable
    return ""

def access_former(field):
    confirmed_fields[field] = True
    return scr_input_form(field, "#1891ac")
def error_former(field, error_name=None):
    confirmed_fields[field] = False
    scr = scr_input_form(field, "red")
    if error_name == None: return scr
    return scr + spanned(error_name)
# функция для выбора параметров скрипта js
def scr_input_form(name, color):
    return f'<script>changeInputBorderColor("{name}", "{color}");</script>'
def spanned(str):
    return f"<span class=\"displaying\" style=\"display:none\">{str}</span>"
# функция для проверки имени или фамилии
def normal_str(str):
    return bool(re.match(r"^[А-Яа-я]+$", str))
# функция для проверки почты
def normal_email(email):
    return bool(re.match(r'^[\w\.-]+@[A-Za-zА-Яа-я\d\.-]+\.[A-Za-zА-Яа-я]{2,6}$', email))
# функция для проверки пароля на допустимые символы
def normal_pass(password):
    return bool(re.match(r"^[A-Za-z\d@$!%*?&]+$", password))

if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
    
    