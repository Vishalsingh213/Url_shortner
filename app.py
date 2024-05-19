from flask import Flask, render_template, request, redirect
from mysql.connector import connect
import random
import string

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/<url>')
def dynamicUrl(url):
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur = connection.cursor()
    query1 = "select * from urlinfo where encryptedUrl='{}'".format(url)
    cur.execute(query1)
    orignalurl = cur.fetchone()
    if orignalurl == None:
        return render_template('index.html')
    print(orignalurl[1])
    return redirect(orignalurl[1])


@app.route('/urlshortner')
def urlshortner():
    # letter='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    url = request.args.get('link')
    custom = request.args.get('customurl')
    print(custom)
    print('planet tech')
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur = connection.cursor()
    encryptedurl = ''
    if custom == '':
        while True:
            encryptedurl = createEncrytedUrl()
            query1 = "select * from urlinfo where encryptedUrl='{}'".format(encryptedurl)
            cur.execute(query1)
            xyz = cur.fetchone()
            if xyz == None:
                break
            finalencryptedurl = 'sd.in/' + encryptedurl
    else:
        query1 = "select * from urlinfo where encryptedUrl='{}'".format(custom)
        cur.execute(query1)
        xyz = cur.fetchone()
        if xyz == None:
            query = "insert into urlinfo(originalurl,encryptedUrl,is_Active) values('{}','{}',1)".format(url, custom)
            cur = connection.cursor()
            cur.execute(query)
            connection.commit()
            finalencryptedurl = 'sd.in/' + custom
        else:
            return ('url already exist')
    return render_template('index.html', finalencryptedurl=finalencryptedurl, url=url)


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/signup')
def signup():
    firstname = request.args.get('first_name')
    lastname = request.args.get('last_name')
    email = request.args.get('email')
    password = request.args.get('password')
    print(firstname)
    connection=connect(host='localhost',database='student',user='root',password='2219')
    cur=connection.cursor()
    print(lastname)
    query="select email from registration where email='{}'".format(email)
    cur.execute(query)
    result=cur.fetchone()
    if result==None:
        query = "insert into registration values('{}','{}','{}','{}')".format(firstname,lastname,email,password)
        cur=connection.cursor()
        cur.execute(query)
        connection.commit()
        return render_template('login.html',login='successfully login')

    else:
        return render_template('login.html',login='use are already registered')

@app.route('/login')
def googlelogin():
    return render_template('login.html')

@app.route('/checkLoginIn')
def checkLoginIn():
    email=request.args.get('email')
    password=request.args.get('password')
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur = connection.cursor()
    query1 = "select * from registration where email='{}'".format(email)
    cur.execute(query1)
    xyz = cur.fetchone()
    print(xyz)
    if xyz==None:
        return render_template('login.html',xyz='please enter valid email id')
    else:
        if password==xyz[3]:
            return redirect('/home')
        else:
            return render_template('Login.html', xyz='your password is not correct')


@app.route('/home')
def home():
    connection = connect(host="localhost", database="student", user="root", password="2219")
    cur=connection.cursor()
    query="select * from urlinfo"
    cur.execute(query)
    data=cur.fetchall()
    return render_template('UserHome.html', data=data)


def createEncrytedUrl():
    letter = string.ascii_letters + string.digits
    encryptedurl = ''
    for i in range(6):
        encryptedurl = encryptedurl + ''.join(random.choice(letter))
    print(encryptedurl)
    return encryptedurl


if __name__ == "__main__":
    app.run()
