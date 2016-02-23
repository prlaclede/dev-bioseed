import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from bioseed.modules import *

email_api = Blueprint('email_api', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@email_api.route('/email', methods = ['POST', 'GET'])
def email():
  updatePassword = id_generator(6)
  conn = connectToDB()
  cur = conn.cursor()
  email = request.form['email']
  try:
    update = "UPDATE users SET users.password = PASSWORD(%s) WHERE users.email = %s"
    cur.execute(update, (updatePassword, email))
    conn.commit()
  except:
    print "UPDATE failed"
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login("bioseedforgotpasword@gmail.com", "bioSeedDB")
  try:
    query = "SELECT username, password FROM users WHERE users.email = %s"
    cur.execute(query, (email))
  except:
    print "query Failed"
  user = cur.fetchone()
  msg = "Below you will see your username and password. Please login and change your password \n Username: %s \n Password: %s" % (user[0], updatePassword)
  
  server.sendmail("bioseedforgotpasword@gmail.com", email, msg)
  server.quit()
  conn.close()
  return render_template('loginScreen.html', selectedMenu='Login')