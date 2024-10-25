from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import logging
from datetime import datetime
import os
import locale

# Настройка логирования для авторизации
auth_logger = logging.getLogger('auth')
auth_logger.setLevel(logging.INFO)
handler = logging.FileHandler('auth.log')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
auth_logger.addHandler(handler)




locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
app = Flask(__name__)
secret_key = os.urandom(24)
app.secret_key = secret_key

# Загрузка данных аутентификации
auth_data = pd.read_excel('data/auth.xlsx')

# Загрузка данных приёмов
receptions = pd.read_excel('data/receptions.xlsx')

# Преобразуем типы данных, если нужно
receptions['add_time'] = pd.to_datetime(receptions['add_time'], errors='coerce')
receptions['start_time'] = pd.to_datetime(receptions['start_time'], errors='coerce')
receptions['end_time'] = pd.to_datetime(receptions['end_time'], errors='coerce')
receptions['cancel_time'] = pd.to_datetime(receptions['cancel_time'],
                                           errors='coerce')  # Обработка ошибок преобразования

# Проверка, что все данные в 'patient_id' являются числами, преобразуем к int
receptions['patient_id'] = pd.to_numeric(receptions['patient_id'], errors='coerce').fillna(0).astype(int)

# Заполнение пропущенных значений в зависимости от типа данных
for column in receptions.columns:
    if receptions[column].dtype in ['float64', 'int64']:
        # Для числовых столбцов заменяем NaN на 0
        receptions[column] = receptions[column].fillna(0)
    else:
        # Для остальных (например, строковых) заменяем NaN на пустую строку
        receptions[column] = receptions[column].fillna('')

# Добавление новых столбцов для расчетов
current_date = datetime.now()

# Расчёт дней до приёма и дней после приёма
receptions['days_until_appointment'] = receptions['start_time'].apply(
    lambda x: (x - current_date).days if pd.notnull(x) and x > current_date else ''
)
receptions['days_since_appointment'] = receptions['start_time'].apply(
    lambda x: (current_date - x).days if pd.notnull(x) and x <= current_date else ''
)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    login_phone = request.form['login'].replace(" ", "")  # Убираем пробелы
    password = request.form['password']

    # Преобразуем столбец login в строки
    auth_data['login'] = auth_data['login'].astype(str)

    # Проверка наличия телефона и пароля в auth_data
    if login_phone in auth_data['login'].values:
        user_info = auth_data[auth_data['login'] == login_phone].iloc[0]
        if user_info['password'] == password:
            session['patient_id'] = int(user_info['patient_id'])  # Преобразуем в обычный int
            auth_logger.info(f'Successful login for {login_phone}')  # Логируем успешный вход
            return redirect(url_for('appointments'))
        else:
            auth_logger.warning(f'Failed login attempt for {login_phone}: Incorrect password')  # Логируем неудачный вход
            flash('Ошибка авторизации. Неверный пароль.')
    else:
        auth_logger.warning(f'Failed login attempt for {login_phone}: User not found')  # Логируем неудачный вход
        flash('Ошибка авторизации. Пользователь не найден.')

    return redirect(url_for('index'))


@app.route('/appointments')
def appointments():
    if 'patient_id' not in session:
        return redirect(url_for('index'))

    patient_id = session['patient_id']
    patient_receptions = receptions[receptions['patient_id'] == patient_id]

    # Определение будущих и завершённых приёмов
    upcoming = patient_receptions[patient_receptions['start_time'] > datetime.now()]
    past = patient_receptions[patient_receptions['start_time'] <= datetime.now()]

    # Получение личного и семейного счёта
    if not patient_receptions.empty:
        personal_account = patient_receptions['personal_account'].iloc[0]
        family_account = patient_receptions['family_account'].iloc[0]
    else:
        personal_account = 0
        family_account = 0

    future_appointments = [
        {
            'date': appointment['start_time'].strftime('%d.%m.%Y'),
            'day_of_week': appointment['start_time'].strftime('%a'),
            'time': appointment['start_time'].strftime('%H:%M'),
            'days_until': appointment['days_until_appointment'],
            'doctor': appointment['doctor_fio'],
        } for _, appointment in upcoming.iterrows()
    ]

    past_appointments = [
        {
            'date': appointment['start_time'].strftime('%d.%m.%Y'),
            'day_of_week': appointment['start_time'].strftime('%a'),
            'time': appointment['start_time'].strftime('%H:%M'),
            'days_since': appointment['days_since_appointment'],
            'doctor': appointment['doctor_fio'],
        } for _, appointment in past.iterrows()
    ]

    patients = receptions[['patient_id', 'patient_fio']].drop_duplicates().to_dict(orient='records')
    clinics = receptions[['clinic']].drop_duplicates().rename(columns={'clinic': 'name'}).to_dict(orient='records')


    return render_template('template.html', past_appointments=past_appointments, future_appointments=future_appointments,
                           personal_account=personal_account, family_account=family_account, patients=patients, clinics=clinics)



@app.route('/logout')
def logout():
    session.pop('patient_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
