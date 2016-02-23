import os, datetime, csv, StringIO, flask, smtplib, string, random, MySQLdb, logging
from flask import Flask, render_template, request, session, Blueprint
from bioseed.modules import *

import_api = Blueprint('import_api', __name__)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@import_api.route('/importCSV', methods = ['POST', 'GET'])
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