import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb
from flask import Flask, render_template, request, session

app = Flask(__name__)

app.secret_key = os.urandom(24).encode('hex')

currentUser = ''

def connectToDB():
  try:
    return MySQLdb.connect("localhost", "root", "mysql" , "bioseeddb")
  except:
    print("Can't connect to database")

#This function is used to see of the string contains special chatacters
def stringContains(inputString):
  import re
  if (re.match('^[a-zA-Z0-9-_]*$',inputString)):
    #return true if the string only contains the Above characters
    return True 
  else:
    #return false if the string contains special characters
    return False
  
@app.route('/')
def mainIndex():
    return render_template('index.html')

@app.route('/loginScreen')
def login():
    return render_template('loginScreen.html', selectedMenu='Login')
    
@app.route('/search')
def search():
  return render_template('search.html')
  
@app.route('/forgotPassword')
def forgotPassword():
  print "when do we come herer"
  return render_template('forgotPassword.html')
  
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))  

@app.route('/email', methods = ['POST', 'GET'])
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
  
@app.route('/report')
def report():
  conn = connectToDB()
  cur = conn.cursor()
#  newSearch = '%' + request.form['stock_id'] + '%'
#  newSearch = "123"
  newSearch = request.args.get('stockid')
  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE stock_id = %s"
  # print query
  cur.execute(query, newSearch)
  stockid = cur.fetchone()
  # olddate = stockid[7]
  # date = olddate.split("-")
  conn.commit()
  conn.close()
  return render_template('report.html', stockid = stockid)  

@app.route('/label', methods = ['POST', 'GET'])
def exportLabel():
    if request.form['submit'] == 'Export Label':
      label = request.form['file']
      ID = label.split("_")
      query = "SELECT * FROM seed_stock WHERE stock_id = %s"
      try:
        conn = connectToDB()
        cur = conn.cursor()
        cur.execute(query, ID[0])
        stock = cur.fetchone()
        conn.commit()
      except:
        print "Yes we clicked " + label + " " + ID[0] 

    conn.close()
    return "hello world"

@app.route('/modifyPlant')
def modifyPlant():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch = request.args.get('stockid')
  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE seed_stock.stock_id = %s"
#  query = "SELECT stock_id, cross_id FROM seed_stock WHERE stock_id = %s"
  
  # newStockID = request.form['stock_id']
  # print newStockID
  # newCrossID = request.form['cross_id']
  # print newCrossID

  # try:
  # update = "UPDATE seed_stock,  SET stock_id = %s , cross_id = cross_id(%s)"
  # cur.execute(update, (newStockID, newCrossID))
  cur.execute(query, newSearch)

  # except:
  #   print "UPDATE failed"
    

  # newQuery = "SELECT stock_id, cross_id FROM seed_stock"
  # cur.execute(newQuery)
  stockid = cur.fetchone()
  print stockid
  conn.commit()
  conn.close()
  return render_template('modifyPlant.html', stockid = stockid)    
  
@app.route('/searchDB', methods = ['POST', 'GET'])
def searchDB():
  conn = connectToDB()
  cur = conn.cursor()
  displaySearch = request.form['search_field']
  newSearch =  '%' + displaySearch + '%'
  defaultSearch = '*'
  #seedstock = []
  # query = "SELECT * from seed_stock where stock_id ='" + request.form['search_field'] + "'"
  # query = "SELECT * FROM seed_stock WHERE stock_id LIKE %s OR cross_id LIKE %s OR genotype LIKE %s OR generation LIKE %s OR female_parent LIKE %s OR male_parent LIKE %s OR species LIKE %s OR date_collected LIKE %s OR location LIKE %s OR contributor_id = %s OR antibiotics_resistance LIKE %s OR oligo_1 LIKE %s OR oligo_2 LIKE %s OR notes LIKE %s"
  #defaultQuery = "SELECT * from seed_stock;"
  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE stock_id OR cross_id LIKE %s"
  defaultQuery = "SELECT * from seed_stock;"
  #print query
  if newSearch == '%Enter keywords....%':
    newSearch = "%%"
    #print newSearch
    cur.execute(query, newSearch)
    # with open('output_file.csv', 'wb') as fout:
    #   writer = csv.writer(fout)
    #   writer.writerow([ i[0] for i in cur.description ]) # heading row
    #   writer.writerows(cur.fetchall())
  else:
    print newSearch
    #print "im in here!"
    cur.execute(query, newSearch)
    # with open('output_file.csv', 'wb') as fout:
    #   writer = csv.writer(fout)
    #   writer.writerow([ i[0] for i in cur.description ]) # heading row
    #   writer.writerows(cur.fetchall())
  
  #print query
  seedstock = cur.fetchall()
  # print request.form['search_form']
    # except:
    #   print("Error executing select")
      
  conn.commit()
  conn.close()
  return render_template('search.html', seedstock = seedstock, displaySearch = displaySearch)

@app.route('/importCSV', methods = ['POST', 'GET'])
def importCSV():
  conn = connectToDB()
  cur = conn.cursor()
  # csv_data = csv.reader(file('import.csv'))
  # for row in csv_data:
  #   cur.execute('INSERT INTO seed_stock(stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes)'
  #         'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s", "%s", "%s","%s","%s")', 
  #         row)
#close the connection to the database.
  conn.commit()
  conn.close()
  return "Hello World"
  
@app.route('/outputCSV', methods = ['POST', 'GET'])
def outputCSV():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch =  '%' + request.args.get('search_field') + '%'
  defaultSearch = '*'

  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE stock_id LIKE %s"
  defaultQuery = "SELECT * from seed_stock;"
  # #print query
  si = StringIO.StringIO()
  if newSearch == '%Enter keywords....%':
    newSearch = "%%"
  #   #print newSearch
    cur.execute(query, newSearch)
    # with open('output_file.csv', 'wb') as fout:
    
    writer = csv.writer(si)
    writer.writerow([ i[0] for i in cur.description ]) # heading row
    writer.writerows(cur.fetchall())
  else:
  #   print newSearch
  #   #print "im in here!"
    cur.execute(query, newSearch)
    writer = csv.writer(si)
    writer.writerow([ i[0] for i in cur.description ]) # heading row
    writer.writerows(cur.fetchall())
  
  # #print query
  # seedstock = cur.fetchall()
  # # print request.form['search_form']
  #   # except:
  #   #   print("Error executing select")
      
  conn.commit()
  conn.close()
  
  output = flask.make_response(si.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=export.csv"
  output.headers["Content-type"] = "text/csv"
  
  return output
  

@app.route('/searchDBModify', methods = ['POST', 'GET'])
def searchDBModify():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch =  '%' + request.form['search_field'] + '%'
  defaultSearch = '*'
  #seedstock = []
  # query = "SELECT * from seed_stock where stock_id ='" + request.form['search_field'] + "'"
  # query = "SELECT * FROM seed_stock WHERE stock_id LIKE %s OR cross_id LIKE %s OR genotype LIKE %s OR generation LIKE %s OR female_parent LIKE %s OR male_parent LIKE %s OR species LIKE %s OR date_collected LIKE %s OR location LIKE %s OR contributor_id = %s OR antibiotics_resistance LIKE %s OR oligo_1 LIKE %s OR oligo_2 LIKE %s OR notes LIKE %s"
  #defaultQuery = "SELECT * from seed_stock;"
  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE stock_id LIKE %s"
  defaultQuery = "SELECT * from seed_stock;"
  #print query
  if newSearch == '%Enter keywords....%':
    newSearch = "%%"
    #print newSearch
    cur.execute(query, newSearch)
  else:
    print newSearch
    #print "im in here!"
    cur.execute(query, newSearch)
  
  #print query
  seedstock = cur.fetchall()
  # print request.form['search_form']
    # except:
    #   print("Error executing select")
      
  conn.commit()
  conn.close()
  return render_template('modifySeed.html', seedstock = seedstock)


    
@app.route('/modify')
def modify():
    return render_template('modifyUser.html')    
    

    
@app.route('/modifyUser', methods = ['GET', 'POST'])
def modifyUser():
  conn = connectToDB()
  cur = conn.cursor()
#  newSearch = '%' + request.form['stock_id'] + '%'
#  newSearch = "123"
  newSearch = request.args.get('userId')
  query = "SELECT username, password, active, role, email FROM users, user_role WHERE users.username = %s AND users.user_id = user_role.user_id"
  cur.execute(query, newSearch)
  userId = cur.fetchone()
  conn.commit()
  conn.close()
  
  return render_template('modifyUser.html', userId = userId)  

@app.route('/userSetting', methods = ['GET', 'POST'])
def userSetting():
  conn = connectToDB()
  cur = conn.cursor()
#  newSearch = '%' + request.form['stock_id'] + '%'
#  newSearch = "123"
  newSearch = session['username']
  print newSearch
  query = "SELECT username, password, active, role, email FROM users, user_role WHERE users.username = %s AND users.user_id = user_role.user_id"
  cur.execute(query, newSearch)
  userId = cur.fetchone()
  conn.commit()
  conn.close()
  
  return render_template('userSetting.html', userId = userId)
    
@app.route('/users', methods = ['GET', 'POST'])
def Users():
  conn = connectToDB()
  cur = conn.cursor()
  
  query = "SELECT username, password, active, role, email FROM users, user_role WHERE users.user_id = user_role.user_id"
  cur.execute(query)
  users = cur.fetchall()
  return render_template('users.html', users = users)
    #return render_template('users.html')
    
@app.route('/addUsers')
def addUsers():
  return render_template('addUsers.html', selectedMenu='addUsers')
    
@app.route('/modifySeed')
def modifySeed():
  return render_template('modifySeed.html', selectedMenu='modifySeed')
    
@app.route('/add')
def add():
    return render_template('add.html')
    
@app.route('/addToDB', methods = ['POST'])
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
  #DB_data = cur.fetchall()
  # try:
  #     if(stringContains(newStock_id)):
  #       error = "Stock ID already in Database"
  #       return render_template('add.html', error = error)
  #     else:
  insert = "INSERT INTO seed_stock (stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s, %s)"
        # print insert
  cur.execute(insert, (newStock_id, newCross_id, newGenotype, newGeneration, newFemale_Parent, newMale_Parent, newSpecies, date_collected, newLocation, newContributor_id, newAntibiotics, newOligo1, newOligo2, newNotes))
  #cur.execute(insert)
  conn.commit()
  # except:
  #   print "Error"
    
  conn.close()
  # try:
  #   if (stringContains(newStock_id)):
  #     error = "Stock ID already in Database"
  #     return render_template('add.html', error = error)
  #   else:
  #   # query = "SELECT stock_id FROM seed_stock WHERE stock_id = %s"
  #     insert = "INSERT INTO seed_stock (stockID, crossID, genotype, generation, femaleParent, maleParent, species, location, contributor, antiboticResistance, oligo1, oligo2, notes) VAULES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s ,%s)" 
  #     try:
  #       cur.execute(insert, (newStock_id, newCross_id, newGenotype, newGeneration, newFemale_Parent, newMale_Parent, newSpecies, newLocation, newContributor_id, newAntibiotics, newOligo1, newOligo2, newNotes))
  #       conn.commit()
  #       conn.close()
      # except:
      #   print "Error"
  # conn.close()
  # return render_template('users.html', DB_data = DB_data)
  return render_template('add.html')   
   
@app.route('/searchUser', methods = ['POST'])
def searchUser():
  conn = connectToDB()
  cur = conn.cursor()
  searchName = request.form['search_field']
  query = "SELECT * FROM users NATURAL JOIN user_role WHERE username = %s"
  cur.execute(query, searchName)
  UserInfo = cur.fetchall()
  print UserInfo
  return render_template('modifyUser.html', UserInfo = UserInfo)
    
    
@app.route('/addUserToDB', methods = ['GET', 'POST'])
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


@app.route('/updateUserToDB', methods = ['GET', 'POST'])
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
  

@app.route('/updatePlant', methods = ['GET','POST'])
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
  print newSearch
  # query = "SELECT stock_id, cross_id FROM seed_stock WHERE seed_stock.stock_id = %s"
  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE seed_stock.stock_id = %s"
  # newStockID = request.form['stock_id']
  # print newStockID
  # newCrossID = request.form['cross_id']
  # print newCrossID

  # try:
  # update = "UPDATE seed_stock,  SET stock_id = %s , cross_id = cross_id(%s)"
  # cur.execute(update, (newStockID, newCrossID))
  cur.execute(query, newSearch)
  stock = cur.fetchone
  stockId = stock[0]
  print query
  print stockId
  # update = "UPDATE seed_stock SET cross_id = %s WHERE cross_id = %s"
  
      # Working code
      # update = "UPDATE seed_stock SET cross_id = %s WHERE stock_id = %s"
      # cur.execute(update, (newCrossID, stockId))
  update = "UPDATE seed_stock SET cross_id = %s, genotype = %s WHERE stock_id = %s"
  cur.execute(update, (newCrossID, newGenotype, newGeneration, newFemaleParent, newMaleParent, newSpecies, newLocation, newContributor, newAntibioticResistance, newOligo1, newOligo2, newNotes, stockId))
  # except:
  #   print "UPDATE failed"
    

  # newQuery = "SELECT stock_id, cross_id FROM seed_stock"
  # cur.execute(newQuery)

  conn.commit()
  conn.close()
  
  return render_template('modifySeed.html', stock = stock)

@app.route('/loginAction', methods = ['POST'])
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

@app.route('/modifyStock', methods = ['POST'])
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


@app.route('/logout', methods = ['GET'])
def logout():
    if request.method == 'GET':

      session.pop('username', None)
      session.pop('role', None)
    return render_template('loginScreen.html')

if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8080)
