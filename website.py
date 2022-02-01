#!/usr/bin/python
# -*- encoding:utf-8 -*-

import threading

from flask import Flask, render_template, request, send_file
from ratelimit import limits

from bot import indirbeni_cli
from media_handler import Downloader
from script_random import CollectRandom

app = Flask(__name__, template_folder='static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

down = Downloader()
threading.Thread(target=CollectRandom, daemon=True).start()
threading.Thread(target=indirbeni_cli, daemon=True).start()


_CALLS = 100
_PERIOD = 60

# PAGES


@app.route("/")
@limits(calls=_CALLS, period=_PERIOD)
def get_home():
    return render_template('index.html')


@app.route("/download/<id>", methods=['GET'])
@limits(calls=_CALLS, period=_PERIOD)
def get_file(id):
    type, data = down.handle(id)

    if type == "Text":
        return render_template('code.html', code=data)
    elif type == "File":
        return send_file(data, as_attachment=True)
    elif type == "Unsupported":
        return render_template('unsupported.html')
    else:
        return render_template('invalid.html')


@app.route("/faq")
@limits(calls=_CALLS, period=_PERIOD)
def get_faq():
    return render_template('faq.html')


@app.route('/get_url', methods=['POST'])
@limits(calls=_CALLS, period=_PERIOD)
def get_url():
    url = request.form['redditurl']
    type, data = down.handle(url)
    if type == "Text":
        return render_template('code.html', code=data)
    elif type == "File":
        return send_file(data, as_attachment=True)
    else:
        return render_template('error.html'), 404


@app.route('/get_url', methods=['GET'])
@limits(calls=_CALLS, period=_PERIOD)
def return_none():
    return render_template('error.html'), 404


@app.errorhandler(404)
@limits(calls=_CALLS, period=_PERIOD)
def not_found(error):
    return render_template('error.html'), 404

# IMAGES


@app.route("/logo.png")
@limits(calls=_CALLS, period=_PERIOD)
def logo():
    return app.send_static_file("images/logo.png")


@app.route("/faq.png")
@limits(calls=_CALLS, period=_PERIOD)
def faq():
    return app.send_static_file("images/faq_2.png")


@app.route("/619.png")
@app.route("/download/619.png")
@limits(calls=_CALLS, period=_PERIOD)
def get_invalid():
    return app.send_static_file("images/619.png")


@app.route("/31sj.png")
@app.route("/download/31sj.png")
@limits(calls=_CALLS, period=_PERIOD)
def get_unsupported():
    return app.send_static_file("images/31sj.png")


@app.route('/favicon.ico')
@limits(calls=_CALLS, period=_PERIOD)
def favicon():
    return app.send_static_file("images/favicon.ico")


@app.route("/404.png")
@limits(calls=_CALLS, period=_PERIOD)
def get_404():
    return app.send_static_file("images/404.png")
