from flask import Flask, request
from flask_cors import CORS
import psycopg2
import datetime
import pytz

app = Flask(__name__)

CORS(app)

def saveTransaction(name, rate, accelerometer, barometer, time):
    mydb = psycopg2.connect( host='', user='', password='', dbname="postgres", options="-c search_path=dbo,fitbit" )
    mycursor = mydb.cursor()
    sql = 'INSERT INTO realtime ("user", rate, accelerometer, barometer, "time") VALUES (%s, %s, %s, %s, %s)'
    val = (name, rate, accelerometer, barometer, time)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/data')
def data():
  data = request.args.get('data', default = '|||', type = str)
  datas = data.split('|')
  name = datas[0]
  rate = datas[1]
  accelerometer = datas[2]
  barometer = datas[3]
  e = datetime.datetime.now(pytz.timezone('Pacific/Auckland'))
  if int(rate) != -999:
    saveTransaction(name, rate, accelerometer, barometer, e.strftime("%Y-%m-%d %H:%M:%S"))
  return 'ok'
