import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from views import *

app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')

app.register_blueprint(account_api)
app.register_blueprint(admin_api)
app.register_blueprint(import_api)
app.register_blueprint(download_api)
app.register_blueprint(email_api)

currentUser = ''