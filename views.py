from flask import Flask,render_template,request,redirect,session
import bcrypt
import mysql.connector
import os
import json
from forms import LoginForm,RegisterForm

app = Flask(__name__)
app.secret_key=os.urandom(24)


conn=mysql.connector.connect(host="localhost", user="root",password="", database="users")
cursor=conn.cursor()

@app.route("/")
def login():
    form=LoginForm()
    return render_template('login.html',form = form)


@app.route("/register")
def register():  
    form=RegisterForm()
    return render_template('register.html',form=form)


@app.route("/home")
def home(): 
    if 'id' in session: 
        student_id=session['id']
        cursor.execute("SELECT * FROM register WHERE id = {};".format(student_id))
        data = cursor.fetchall()
        return render_template('home.html', data=data)
    else:
        return redirect('/')


@app.route("/login_validation", methods=['POST'])
def login_validation(): 
    email = request.form.get('email')
    password = request.form.get('password') 
    cursor.execute("select * from `register` where `email` like '{}' and `password` like '{}'".format(email,password))
    register=cursor.fetchall()
    print(register)
    if register[0][6]==None:
        return redirect('/register')
    if len(register)>0:
        session['id']=register[0][0]
        return redirect('/home')
    else:
        return redirect('/')


#@app.route("/add_user/<postData>", methods=['POST'])
@app.route("/add_user/<serverData>/", methods=['POST','GET'])
def add_user(serverData):
    studentData=json.loads(serverData) 
    print("post data is "+serverData)
    name = studentData['name'] 
    rollno = studentData['rollno'] 
    email = studentData['email']
    password = studentData['password'] 
    standard = studentData['standard']
    mark =studentData['marksDetails']
    cursor.execute("""insert into `register` (`name`,`rollno`,`email`,`password`,`standard`,`mark`) values('{}','{}','{}','{}','{}','{}')""".format(name,rollno,email,password,standard,json.dumps(mark)))
    conn.commit()
    #session code
    cursor.execute("""select * from register where `email` like '{}' """.format(email))
    register=cursor.fetchall()
    session['id']=register[0][0]
    return "{status:true}"


@app.route("/logout")
def logout():
    session.pop('id')
    return redirect('/') 


if __name__ == "__main__":
    app.run(debug=True)