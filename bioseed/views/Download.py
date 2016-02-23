import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from bioseed.modules import *

download_api = Blueprint('download_api', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@download_api.route('/report')
def report():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch = request.args.get('stockid')
  query = """SELECT stock_id, cross_id, genotype, generation, female_parent, 
  male_parent, species, date_collected, location, contributor_id, 
  antibiotics_resistance, oligo_1, oligo_2, 
  notes FROM seed_stock WHERE stock_id = %s"""
  cur.execute(query, newSearch)
  stockid = cur.fetchone()
  conn.commit()
  conn.close()
  return render_template('report.html', stockid = stockid)  
  
@download_api.route('/label', methods = ['POST', 'GET'])
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

@download_api.route('/outputCSV', methods = ['POST', 'GET'])
def outputCSV():
  conn = connectToDB()
  cur = conn.cursor()
  newSearch =  '%' + request.args.get('search_field') + '%'
  defaultSearch = '*'

  query = "SELECT stock_id, cross_id, genotype, generation, female_parent, male_parent, species, date_collected, location, contributor_id, antibiotics_resistance, oligo_1, oligo_2, notes FROM seed_stock WHERE stock_id LIKE %s"
  defaultQuery = "SELECT * from seed_stock;"
  si = StringIO.StringIO()
  if newSearch == '%Enter keywords....%':
    newSearch = "%%"
    cur.execute(query, newSearch)
    
    writer = csv.writer(si)
    writer.writerow([ i[0] for i in cur.description ]) # heading row
    writer.writerows(cur.fetchall())
  else:
    cur.execute(query, newSearch)
    writer = csv.writer(si)
    writer.writerow([ i[0] for i in cur.description ]) # heading row
    writer.writerows(cur.fetchall())
    
  conn.commit()
  conn.close()
  
  output = flask.make_response(si.getvalue())
  output.headers["Content-Disposition"] = "attachment; filename=export.csv"
  output.headers["Content-type"] = "text/csv"
  
  return output