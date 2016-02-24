import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from bioseed.modules import *

account_api = Blueprint('account_api', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

#This function is used to see of the string contains special chatacters
def stringContains(inputString):
  import re
  if (re.match('^[a-zA-Z0-9-_]*$',inputString)):
    #return true if the string only contains the Above characters
    return True 
  else:
    #return false if the string contains special characters
    return False

@account_api.route('/loginScreen')
def login():
    return render_template('loginScreen.html', selectedMenu='Login')
    
@account_api.route('/forgotPassword')
def forgotPassword():
  return render_template('forgotPassword.html')
  
@account_api.route('/searchDB', methods = ['POST', 'GET'])
def searchDB():
  conn = connectToDB()
  cur = conn.cursor()
  displaySearch = request.form['search_field']
  newSearch =  '%' + displaySearch + '%'
  defaultSearch = '*'

  query = """SELECT stock_id, cross_id, genotype, generation, female_parent, 
  male_parent, species, date_collected, location, contributor_id, 
  antibiotics_resistance, oligo_1, oligo_2, 
  notes FROM seed_stock WHERE stock_id OR cross_id LIKE %s"""
  defaultQuery = "SELECT * from seed_stock;"
  #print query
  if newSearch == '%Enter keywords....%':
    newSearch = "%%"
    cur.execute(query, newSearch)
  else:
    print newSearch
    cur.execute(query, newSearch)
    
  seedstock = cur.fetchall()

  conn.commit()
  conn.close()
  return render_template('search.html', seedstock = seedstock, displaySearch = displaySearch)
  
@account_api.route('/searchDBModify', methods = ['POST', 'GET'])
def searchDBModify():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch =  '%' + request.form['search_field'] + '%'
  defaultSearch = '*'
  query = """SELECT stock_id, cross_id, genotype, generation, 
  female_parent, male_parent, species, date_collected, location, 
  contributor_id, antibiotics_resistance, oligo_1, oligo_2, 
  notes FROM seed_stock WHERE stock_id LIKE %s"""
  defaultQuery = "SELECT * from seed_stock;"
  if newSearch == '%Enter keywords....%':
    newSearch = "%%"
    cur.execute(query, newSearch)
  else:
    print newSearch
    cur.execute(query, newSearch)
    
  seedstock = cur.fetchall()
      
  conn.commit()
  conn.close()
  return render_template('modifySeed.html', seedstock = seedstock)
 
@account_api.route('/userSetting', methods = ['GET', 'POST'])
def userSetting():
  conn = connectToDB()
  cur = conn.cursor()
  
  newSearch = session['username']
  print newSearch
  query = "SELECT username, password, active, role, email FROM users, user_role WHERE users.username = %s AND users.user_id = user_role.user_id"
  cur.execute(query, newSearch)
  userId = cur.fetchone()
  conn.commit()
  conn.close()
  
  return render_template('userSetting.html', userId = userId)
 
@account_api.route('/add')
def add():
    return render_template('add.html')
  
@account_api.route('/modifySeed')
def modifySeed():
  return render_template('modifySeed.html', selectedMenu='modifySeed')
  
  
@account_api.route('/addToDB', methods = ['POST'])
def addToDB():
  conn = connectToDB()
  cur = conn.cursor()
  newStock_id = request.form['stockID']
  newCross_id = request.form['crossID']
  newGenotype = request.form['genotype']
  newGeneration = request.form['generation']
  newFemale_Parent = request.form['femaleParent']
  newMale_Parent = request.form['maleParent']
  newSpecies = request.form['species']
  yearNow = request.form['year']
  monthNow = request.form['month']
  dayNow = request.form['day']
  date_collected = yearNow + "-" + monthNow + "-" + dayNow
  newLocation = request.form['location']
  newContributor_id = request.form['contributor']
  newAntibiotics = request.form['antibioticResistance']
  newOligo1 = request.form['oligo1']
  newOligo2 = request.form['oligo2']
  newNotes = request.form['notes']

  insert = "INSERT INTO seed_stock (stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)"

  cur.execute(insert, (newStock_id, newCross_id, newGenotype, newGeneration, newFemale_Parent, newMale_Parent, newSpecies, date_collected, newLocation, newContributor_id, newAntibiotics, newOligo1, newOligo2, newNotes))

  conn.commit()
    
  conn.close()

  return render_template('add.html') 
  
@account_api.route('/updatePlant', methods = ['GET','POST'])
def updatePlant():
  conn = connectToDB()
  cur = conn.cursor()
  newCrossID = request.form['cross_id']
  newGenotype = request.form['genotype']
  newGeneration = request.form['generation']
  newFemaleParent = request.form['femaleParent']
  newMaleParent = request.form['maleParent']
  newSpecies = request.form['species']
  # DATE
  newLocation = request.form['location']
  newContributor = request.form['contributor']
  newAntibioticResistance = request.form['antibioticResistance']
  newOligo1 = request.form['oligo1']
  newOligo2 = request.form['oligo2']
  newNotes = request.form['notes']  
  newSearch = request.args.get('stockid')
  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE seed_stock.stock_id = %s"
  cur.execute(query, newSearch)
  stock = cur.fetchone
  stockId = stock[0]
  print query
  print stockId

  update = "UPDATE seed_stock SET cross_id = %s, genotype = %s WHERE stock_id = %s"
  cur.execute(update, (newCrossID, newGenotype, newGeneration, newFemaleParent, newMaleParent, newSpecies, newLocation, newContributor, newAntibioticResistance, newOligo1, newOligo2, newNotes, stockId))

  conn.commit()
  conn.close()
  
  return render_template('modifySeed.html', stock = stock)
  
@account_api.route('/loginAction', methods = ['POST'])
def login_action():
  conn = connectToDB()
  cur = conn.cursor()
  error = None
  error2 = None
  uname = request.form['username']
  pword = request.form['password']
  #acct = request.form['active']
  if(stringContains(uname) and stringContains(pword)):
    query = "SELECT username, password, active, role FROM users, user_role WHERE username = %s and password = PASSWORD(%s) AND users.user_id = user_role.user_id" #%(uname, pword)
    try:
      cur.execute(query, (uname, pword))
      loginQuery = cur.fetchall()
      
      if loginQuery:
        for login in loginQuery:
            session['username'] = uname
            session['role'] = login[3]
            print login[2]
            if login[2] == 1:
              return render_template('search.html')
            else:
              error2 = "your account is not active"
              print "your account is not active"
            return render_template('loginScreen.html', error2 = error2)
      else:
        error = "username or password are incorrect"
        print "username or password are incorrect"
        return render_template('loginScreen.html', error = error)
    except:
      print('login query failed')
  else:
    error = "username or password are incorrect"
    print "how bout here?"
    
  conn.close()
  return render_template('loginScreen.html', error = error)
 
@account_api.route('/modifyStock', methods = ['POST'])
def modifyStock():
  newStock_id = request.form['stockID']
  newCross_id = request.form['crossID']
  newGenotype = request.form['genotype']
  newGeneration = request.form['generation']
  newFemale_Parent = request.form['femaleParent']
  newMale_Parent = request.form['maleParent']
  newSpecies = request.form['species']
  newLocation = request.form['location']
  newContributor_id = request.form['contributor']
  newAntibiotics = request.form['antibioticResistance']
  newOligo1 = request.form['oligo1']
  newOligo2 = request.form['oligo2']
  newNotes = request.form['notes']
  
  update = "UPDATE seed_stock SET cross_id = %s, genotype = %s, generation = %s, female_parent = %s, male_parent = %s, species = %s, location = %s, contributor_id = %s, antibiotics_resistance = %s, oligo_1 = %s, oligo_2 = %s, notes = %s WHERE stock_id = %s"
  try:
    conn = connectToDB()
    cur = conn.cursor()
    cur.execute(update, (newCross_id, newGenotype, newGeneration, newFemale_Parent, newMale_Parent, newSpecies, newLocation, newContributor_id, newAntibiotics, newOligo1, newOligo2, newNotes, newStock_id))
    conn.commit()
  except:
    print "update Failed"
  
  conn.close()
  return render_template("search.html")
  
@account_api.route('/logout', methods = ['GET'])
def logout():
    if request.method == 'GET':

      session.pop('username', None)
      session.pop('role', None)
    return render_template('loginScreen.html')