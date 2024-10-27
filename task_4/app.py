from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os

app = Flask(__name__)

default_url = "https://renident.ru/"
current_url = default_url


# Функция для создания QR-кода
def generate_qr_code(url):
    qr = qrcode.make(url)
    qr.save(os.path.join('static', 'qr_code.png'))


generate_qr_code(current_url)


# Главная страница с QR-кодом
@app.route('/', methods=['GET', 'POST'])
def qr_code_page():
    global current_url

    if request.method == 'POST':
        new_url = request.form['new_url']
        if new_url:
            current_url = new_url
            generate_qr_code(current_url)

    return render_template('qr_code_page.html', current_url=current_url)


if __name__ == '__main__':
    app.run(debug=True)
