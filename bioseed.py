from bioseed import *

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

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080) 