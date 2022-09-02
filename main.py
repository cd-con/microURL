import binascii

import flask
import requests
import base64
from flask import Flask, render_template, request

domainName = "127.0.0.1:5000"

app = Flask(__name__, template_folder="resources", static_folder="static")

def check_page_status(url):
    try:
        with requests.request("GET", "http://" + url) as requestData:
            return requestData.status_code == 200
    except requests.RequestException as e:
        print(f"[DEBUG] Checking page operation failed! Error: {e}")


def deobfuscate_url(base64string):
    try:
        return base64.urlsafe_b64decode(base64string.encode('utf-8')).decode("utf-8")
    except binascii.Error as _:
        return "Введёная ссылка не является рабочей"


def obfuscate_url(url):
    if check_page_status(url):
        return domainName + "/" + base64.urlsafe_b64encode(url.encode('utf-8')).decode("utf-8")
    else:
        return domainName


@app.route('/<string:shorten_url>', methods=['GET'])
def redirect_user(shorten_url):
    return flask.redirect("http://" + deobfuscate_url(shorten_url), code=302)


@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method == 'POST':
        return render_template('landpage.html', message=f"Ваша ссылка: {obfuscate_url(request.form.get('url'))})
    if request.method == 'GET':
        return render_template('landpage.html', message="Введите ссылку на ресурс")

if __name__ == '__main__':
    app.run()
