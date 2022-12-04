from flask import Flask, request
from flask_cors import CORS
import psycopg2
import datetime
import pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText                    
from email.mime.application import MIMEApplication
import timeout_decorator

app = Flask(__name__)

CORS(app)

host = "hwsmtp.exmail.qq.com"
port = 465
email = "admin@iceloof.com"
admin = "admin@iceloof.com"
password = "pyqhaq-qyxwo2-ciGnyh"
to = "hurin@live.ca"
count = 0

def sendEmail(info):
    html = "<html><head><title>Error</title></head><body style='font-family: Comic Sans MS'><p>"+info+"</p><br><p>Kind regards, <br>Iceloof Inc.<br><a href=\"https://www.iceloof.com\">https://www.iceloof.com</a></p></body></html>"
    print('Email send to hurin@live.ca '+html)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = "Fitbit Alert"
    msg['From'] = "Iceloof Admin<"+admin+">"
    msg['Bcc'] = to
    msg['X-Priority'] = '1'
    part2 = MIMEText(html, 'html')
    msg.attach(part2)
    s = smtplib.SMTP_SSL(host=host,port=port)
    s.ehlo()
    s.login(email,password)
    s.sendmail(msg['From'], msg['Bcc'], msg.as_string())
    s.quit()
    print('Email send to '+to)

def saveTransaction(name, rate, accelerometer, barometer, time):
    mydb = psycopg2.connect( host='192.168.1.180', user='fitbit', password='fitbit', dbname="postgres", options="-c search_path=dbo,fitbit" )
    mycursor = mydb.cursor()
    sql = 'INSERT INTO realtime ("user", rate, accelerometer, barometer, "time") VALUES (%s, %s, %s, %s, %s)'
    val = (name, rate, accelerometer, barometer, time)
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    
@app.route('/')
def hello():
    #sendEmail('Doris\'s HR too high ')
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
  if int(rate) >= 120 and int(rate) <= 140:
    if count == 0 or count > 19:
      sendEmail('Doris\'s HR too high '+str(rate))
      count = 1
    else:
      count += 1
      if count >= 19:
        count = 0
  elif int(rate) != -999 and int(rate) <= 45:
    if count == 0 or count > 19:
      sendEmail('Doris\'s HR too low '+str(rate))
      count = 1
    else:
      count += 1
      if count >= 19:
        count = 0
  else:
    count += 1
    if count >= 240:
      count = 0
  return 'ok'
