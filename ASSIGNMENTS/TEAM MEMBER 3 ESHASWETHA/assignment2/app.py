from flask import Flask,render_template,request,url_for
#pipfrom flask_db2 import DB2
import ibm_db
app=Flask(__name__)
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
@app.route('/',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username=request.form['username']
        password = request.form['password']
        roll = request.form['roll']
        try:
            insert_sql = "INSERT INTO REGISTER VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, password)
            ibm_db.bind_param(prep_stmt, 4, roll)
            ibm_db.execute(prep_stmt)
            print("No of Affected rows: ",ibm_db.num_rows(prep_stmt))
        except:
            print("Error: ",ibm_db.stmt_errormsg())
    return render_template("register.html")
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')   
        sql = "SELECT * FROM user REGISTER email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        if account:
            if (password == str(account['PASS']).strip()):
                return render_template('register.html')
            else:
                return render_template('login.html', msg="Password is invalid")
        else:
            return render_template('welcome.html')
    else:
        return render_template('login.html')
@app.route('/login')
def welcome():
    return render_template('welcome.html')
if __name__=='main':
    app.run(debug=True)