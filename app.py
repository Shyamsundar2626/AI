from re import X
from time import time
import pymysql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from datetime import date
from datetime import datetime
import json
from flask import jsonify
from flask_cors import CORS

from flask import Flask
app = Flask(__name__)
CORS(app)

# make sure the username, password and database name are correct
username = 'root'
password = ''
userpass = 'mysql+pymysql://' + username + ':' + password + '@'
# keep this as is for a hosted website
server  = '127.0.0.1'
# change to YOUR database name, with a slash added as shown
dbname   = '/wall-mart-data'
# no socket


# change NOTHING below

# put them all together as a string that shows SQLAlchemy where the database is
app.config['SQLALCHEMY_DATABASE_URI'] = userpass + server + dbname

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

@app.route('/')
def serverStatus():
    return 'Server is up'

@app.route('/data/<age>/<int:gender>/<int:type>')
def savedata(age,gender,type):
    print (age)
    print (gender)
    print (type)
    tdate = date.today()
    ttime = datetime.now()
    print (tdate)
    print (ttime)
    sql = text('INSERT INTO entry_persons (age,gender,type,date,time) VALUES ("'+str(age)+'","'+str(gender)+'","'+str(type)+'","'+str(tdate)+'","'+str(ttime)+'")')
    result = db.engine.execute(sql)
    return 'This is Home '  

@app.route('/getalldata')
def alldata():
   sql = text('SELECT * FROM entry_persons')
   result = db.engine.execute(sql)
   rawdata = result.fetchall()
   
   jsondata = jsonify( [dict(row) for row in rawdata])
   return jsondata

@app.route('/getdatabymonth')
def databymonth():
    month = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sep','Oct','Nov','Dec']
    x = ''
    for m in range(1,13):
        sql = text('SELECT Month(date) AS Month FROM entry_persons WHERE Month(date) = '+str(m))
        result = db.engine.execute(sql)
        rawdata = result.fetchall()
        rawdatalength = len(rawdata)
        ##+str(month[m-1])+
        x+=  '{"month":"'+str(rawdatalength)+'"},'
        
  
    
    x = x[:-1]
    
    rawjson = '['+x+']'
    print(rawjson)
    
    
    
    return rawjson
     
     

if __name__ == '__main__':
   app.run()


