import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from bioseed.modules import *

admin_api = Blueprint('admin_api', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@admin_api.route('/modify')
def modify():
    return render_template('modifyUser.html')    

@admin_api.route('/modifyPlant')
def modifyPlant():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch = request.args.get('stockid')
  query = """SELECT stock_id, cross_id, genotype, generation, female_parent, 
  male_parent, species, date_collected, location, contributor_id, 
  antibiotics_resistance, oligo_1, oligo_2, 
  notes FROM seed_stock WHERE seed_stock.stock_id = %s"""
  cur.execute(query, newSearch)

  stockid = cur.fetchone()
  print stockid
  conn.commit()
  conn.close()
  return render_template('modifyPlant.html', stockid = stockid)  
  
@admin_api.route('/modifyUser', methods = ['GET', 'POST'])
def modifyUser():
  conn = connectToDB()
  cur = conn.cursor()

  newSearch = request.args.get('userId')
  query = "SELECT username, password, active, role, email FROM users, user_role WHERE users.username = %s AND users.user_id = user_role.user_id"
  cur.execute(query, newSearch)
  userId = cur.fetchone()
  conn.commit()
  conn.close()
  
  return render_template('modifyUser.html', userId = userId)  
  
@admin_api.route('/addUsers')
def addUsers():
  return render_template('addUsers.html', selectedMenu='addUsers')
  
@admin_api.route('/users', methods = ['GET', 'POST'])
def Users():
  conn = connectToDB()
  cur = conn.cursor()
  
  query = "SELECT username, password, active, role, email FROM users, user_role WHERE users.user_id = user_role.user_id"
  cur.execute(query)
  users = cur.fetchall()
  return render_template('users.html', users = users)

@admin_api.route('/searchUser', methods = ['POST'])
def searchUser():
  conn = connectToDB()
  cur = conn.cursor()
  searchName = request.form['search_field']
  query = "SELECT * FROM users NATURAL JOIN user_role WHERE username = %s"
  cur.execute(query, searchName)
  UserInfo = cur.fetchall()
  print UserInfo
  return render_template('modifyUser.html', UserInfo = UserInfo)
  
@admin_api.route('/addUserToDB', methods = ['GET', 'POST'])
def addUserToDB():
  #if request.method == 'POST':
  
  conn = connectToDB()
  cur = conn.cursor()
  newUsername = request.form['username']
  newEmail = request.form['email']
  newPassword = request.form['password']
  newAccountType = request.form['accountLevel']
  active = request.form['active']
  if(active == "active"):
    isActive = 1
  else:
    isActive = 0
  if(newAccountType == "Admin"):
    accountType = 0
  elif(newAccountType == "Priviledged"):
    accountType = 1
  else:
    accountType = 2
  if(stringContains(newUsername) and stringContains(newPassword)):
    query = "select * from users WHERE username = %s"# AND password = %s"#crypt(%s)"
    #cur.execute(query, (newUsername, newPassword))
    try:
      if(cur.execute(query, newUsername)):
        error = "Username is already in use"
        return render_template('addUsers.html', error = error)
      else:
        insert = "INSERT INTO users (username, password, active, email) VALUES( %s, PASSWORD(%s), %s, %s)"
        try:
          cur.execute(insert, (newUsername, newPassword, isActive, newEmail))
          conn.commit()
        except:
          print "Error inserting username and password"
        try:
          query = "SELECT * FROM users WHERE username = %s"
          cur.execute(query, (newUsername))
          tests = cur.fetchall()
          print tests
          for test in tests:
            try:
              
              insert = "INSERT INTO user_role(user_id, role) VALUES(%s, %s)"
              cur.execute(insert, (test[0], accountType))
              conn.commit()
            except:
              print test[0]
              print "Error Inserting into user_role"
        except:
         print "error querying newUsername"
    except:
      print "Error querying data"
  else:
    conn.close()
    print 'username is false'
  print "did this work"
  newQuery = "SELECT username, password, active, role FROM users, user_role WHERE users.user_id = user_role.user_id"
  cur.execute(newQuery)
  users = cur.fetchall()
  conn.close()
  
  return render_template('users.html', users = users)


@admin_api.route('/updateUserToDB', methods = ['GET', 'POST'])
def updateUserToDB():
  
  conn = connectToDB()
  cur = conn.cursor()
  newUsername = request.form['username']
  newEmail = request.form['email']
  newPassword = request.form['password']
  newAccountType = request.form['accountLevel']
  active = request.form['active']
  if(active == "active"):
    isActive = 1
  else:
    isActive = 0
  if(newAccountType == "Admin"):
    accountType = 0
  elif(newAccountType == "Priviledged"):
    accountType = 1
  else:
    accountType = 2
  try:
    query = "SELECT password FROM users WHERE username = %s"
    cur.execute(query, (newUsername))
    users = cur.fetchone()
    if users[0] == newPassword:
      update = "UPDATE users, user_role SET username = %s , active = %s, role = %s, email = %s WHERE username = %s AND users.user_id = user_role.user_id"
      cur.execute(update, (newUsername, isActive, accountType, newEmail, newUsername))
      conn.commit()
    else:
      update = "UPDATE users, user_role SET username = %s , password = PASSWORD(%s), active = %s, role = %s, email = %s WHERE username = %s AND users.user_id = user_role.user_id"
      cur.execute(update, (newUsername, newPassword, isActive, accountType, newEmail, newUsername))
      conn.commit()
  except:
    print "update Failed"
  
  return render_template('search.html')
