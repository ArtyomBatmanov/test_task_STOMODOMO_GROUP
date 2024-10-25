from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import logging
from datetime import datetime

# Настройка логирования
logging.basicConfig(filename='auth.log', level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Задайте свой секретный ключ

# Загрузка данных аутентификации
auth_data = pd.read_excel('auth.xlsx')
# Загрузка данных приёмов
receptions = pd.read_excel('receptions.xlsx')

# Преобразуем типы данных, если нужно
receptions['add_time'] = pd.to_datetime(receptions['add_time'])
receptions['start_time'] = pd.to_datetime(receptions['start_time'])
receptions['end_time'] = pd.to_datetime(receptions['end_time'])
receptions['cancel_time'] = pd.to_datetime(receptions['cancel_time'],
                                           errors='coerce')  # Обработка ошибок преобразования
receptions['patient_id'] = receptions['patient_id'].astype(int)

# Замена отсутствующих значений
receptions.fillna('', inplace=True)

# Добавление новых столбцов для расчетов
current_date = datetime.now()
receptions['days_until_appointment'] = receptions['start_time'].apply(
    lambda x: (x - current_date).days if x > current_date else ''
)
receptions['days_since_appointment'] = receptions['start_time'].apply(
    lambda x: (current_date - x).days if x <= current_date else ''
)


@app.route('/')
def index():
    return render_template('login.html')  # Страница аутентификации


@app.route('/login', methods=['POST'])
def login():
    login_phone = request.form['login']
    password = request.form['password']

    # Проверка наличия телефона и пароля в auth_data
    if login_phone in auth_data['login'].values:
        user_info = auth_data[auth_data['login'] == login_phone].iloc[0]
        if user_info['password'] == password:
            session['patient_id'] = user_info['patient_id']
            logging.info(f'Successful login for {login_phone}')
            return redirect(url_for('appointments'))
        else:
            logging.warning(f'Failed login attempt for {login_phone}: Incorrect password')
            flash('Ошибка авторизации. Неверный пароль.')
    else:
        logging.warning(f'Failed login attempt for {login_phone}: User not found')
        flash('Ошибка авторизации. Пользователь не найден.')

    return redirect(url_for('index'))


@app.route('/appointments')
def appointments():
    if 'patient_id' not in session:
        return redirect(url_for('index'))

    patient_id = session['patient_id']
    patient_receptions = receptions[receptions['patient_id'] == patient_id]

    # Определение будущих и завершённых приёмов
    upcoming = patient_receptions[patient_receptions['start_time'] > current_date]
    past = patient_receptions[patient_receptions['start_time'] <= current_date]

    return render_template('template.html', upcoming=upcoming, past=past)


@app.route('/logout')
def logout():
    session.pop('patient_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
