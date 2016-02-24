import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from flask.ext.assets import Environment, Bundle
from views import *
from modules import *

app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')

app.register_blueprint(account_api)
app.register_blueprint(admin_api)
app.register_blueprint(import_api)
app.register_blueprint(download_api)
app.register_blueprint(email_api)


assets = Environment(app)

pluginJS = Bundle('js/plugins/*.js')
customJS = Bundle('js/custom/*.js')

pluginCSS = Bundle('css/plugin/*.css')
customCSS = Bundle('css/custom/*.css')

allJS = Bundle(pluginJS, customJS)
allCSS = Bundle(customCSS, pluginCSS)

assets.register('allJS', allJS)
assets.register('allCSS', allCSS)

