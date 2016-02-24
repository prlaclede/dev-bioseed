import MySQLdb

def connectToDB():
  try:
    return MySQLdb.connect("localhost", "root", "mysql" , "bioseeddb")
  except:
    print("Can't connect to database")