import csv
from datetime import datetime

#from flask_db2 import DB2
#import ibm_db
import ibm_db
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, url_for
import os
#import sendgrid
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import *


dsn_hostname = "0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud"
dsn_uid = "why11914"
dsn_pwd = "qMCrggTKEsZ8b54q" 
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"  
dsn_port = "31198"  
dsn_protocol = "TCPIP"  
dsn_security = "SSL"
dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY={7};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd,dsn_security)

conn = ibm_db.connect(dsn, "", "")

print(conn)
print("Connection Successful............")
app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template("index.html")
@app.route('/jobseeker',methods=['POST','GET'])
def jobseeker():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        skills = request.form['skills']
        expectedjob = request.form['expectedjob']

        #if password!=cp:
            #return render_template('register.html')

        try:
            insert_sql = "INSERT INTO REGISTER_AS_REGISTER VALUES (?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, name)
            ibm_db.bind_param(prep_stmt, 2, email)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.bind_param(prep_stmt, 4, age)
            ibm_db.bind_param(prep_stmt, 5, skills)
            ibm_db.bind_param(prep_stmt, 6, expectedjob)
            ibm_db.execute(prep_stmt)
            #sql = "insert into REGISTER_AS_REGISTER values ('{}','{}','{}','{}','{}','{}')".format( name, email, password, age, skills, expectedjob)
            #stmt = ibm_db.exec_immediate(conn,sql)
            print("No of Affected rows: ",ibm_db.num_rows(prep_stmt))
        except:
            print("Error: ",ibm_db.stmt_errormsg())
    return render_template("registerasjobseeker.html")
@app.route('/organization',methods=['POST','GET'])
def organization():
    if request.method == 'POST':
        organization_name = request.form['organization_name']
        job_role = request.form['job_role']
        lpa = request.form['lpa']
        #address = request.form['address']
        city = request.form['city']
        email = request.form['email']
        mobile = request.form['mobile']

        #if password!=cp:
            #return render_template('register.html')

        try:
            insert_sql = "INSERT INTO REGISTER_AS_ORGANIZATION VALUES (?,?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, organization_name)
            ibm_db.bind_param(prep_stmt, 2, job_role)
            ibm_db.bind_param(prep_stmt, 3, lpa)
            ibm_db.bind_param(prep_stmt, 4, city)
            ibm_db.bind_param(prep_stmt, 5, email)
            ibm_db.bind_param(prep_stmt, 6, mobile)
            ibm_db.execute(prep_stmt)
            #sql = "insert into REGISTER_AS_REGISTER values ('{}','{}','{}','{}','{}','{}')".format( name, email, password, age, skills, expectedjob)
            #stmt = ibm_db.exec_immediate(conn,sql)
            print("No of Affected rows: ",ibm_db.num_rows(prep_stmt))
        except:
            print("Error: ",ibm_db.stmt_errormsg())
    return render_template("registerasorganization.html")
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM REGISTER_AS_REGISTER email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            if (password == str(account['PASS']).strip()):
                return render_template('index.html')
            else:
                return render_template('index.html', msg="Password is invalid")
        else:
            return render_template('registerasjobseeker.html')
    else:
        return render_template('login.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')
@app.route('/apply_job')
def apply_job():
    return render_template('apply_job.html')
@app.route('/applyforjob',methods=['POST','GET'])
def applyforjob():
    if request.method == 'POST':
        resume = request.form.get('resume')
        email = request.form.get('email')
        #message = Mail(from_email=email,to_emails='mail2himaraj@gmail.com',subject='Resume',html_content=resume)
        #sg = SendGridAPIClient('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')
        #response = sg.send(message)
        #return response
        '''sg = sendgrid.SendGridAPIClient(apikey='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')
        from_email=Email("mail2himaraj@gmail.com")
        to_email=Email("mail2himaraj@gmail.com")
        subject="mail"
        content=Content("text/plain","easy")
        mail=Mail(from_email,subject,to_email,content)
        response=sg.client.mail.send.post(request_body=mail.get())'''
    return render_template('upload_resume.html')
@app.route('/manualrecommendation',methods=['POST','GET'])
def manualrecommendation():
    if request.method == 'POST':
        jobrole= request.form.get('jobrole')
        location= request.form.get('location')
        #template='https://www.indeed.com/jobs?q={}&l={}&from=searchOnHP'
        template='https://in.indeed.com/jobs?q={}&l={}&from=searchOnHP'
        url=template.format(jobrole, location)
        return url 
    return render_template('manual.html')
#url=manualrecommendation('jobrole','location')
#print(url)
@app.route('/chatbotrecommendation')
def chatbotrecommendation():
    return render_template("chatbot.html")
@app.route('/chatbotrecon')
def chatbotcon():
    return render_template("chatconversation.html")
if __name__=="__main__":
    port=int(os.environ.get('PORT',5000))
    app.run(port=port,host="0.0.0.0")