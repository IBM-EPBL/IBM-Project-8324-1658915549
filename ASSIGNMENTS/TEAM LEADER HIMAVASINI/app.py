from flask import Flask,render_template,request
import ibm_db
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31198;PROTOCOL=TCPIP;UID=why11914;PWD=qMCrggTKEsZ8b54q;", "", "")
    print("Connected to database")
except:
    print("Failed to connecting: ", ibm_db.conn_errormsg())
app=Flask(__name__)
@app.route('/',methods=["GET","POST"])
def Register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['age']
        Register_No = request.form['Register_no']
        password = request.form['password']

        #if password!=cp:
            #return render_template('register.html')

        try:
            sql = "INSERT into User values ('{}', '{}','{}', '{}')".format( username, email,Register_no, password)
            stmt = ibm_db.exec_immediate(conn,sql)
            print("No of Affected rows: ",ibm_db.num_rows(stmt))
        except:
            print("Error: ",ibm_db.stmt_errormsg())
    return render_template('register.html')
@app.route('login',methods=["GET","POST"])
def login():
     if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        
        try:
            sql = "SELECT * from user where username='{0}' and password='{1}'".format(username,password)
            print(sql)
            stmt = ibm_db.exec_immediate(conn, sql)
            res = ibm_db.fetch_assoc(stmt)
            print(res['USERNAME'])

            if len(res) == 0 :
                return render_template('login.html',message="Incorrect Username/Password")
        except:
            print("Error: ",ibm_db.stmt_errormsg())
        return render_template('login.html')
@app.route('welcome')
def welcome():
    return render_template('welcome.html')

if __name__=="__main__":
    app.run(debug=True)
