#from Scripts.bottle import request
from flask import Flask, render_template, flash, request,session,send_file
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug import secure_filename
import mysql.connector
#import string
#import hashlib
#import base64
#import os
#from io import BytesIO
#import datetime



import tkinter.messagebox
#import os, shutil

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
@app.route("/")
def home():
            return render_template('index.html')
@app.route("/admin")
def admin():
            return render_template('admin.html')
@app.route("/lawyer")
def lawyer():
            return render_template('lawyer.html')
@app.route("/user")
def user():
            return render_template('user.html')
@app.route("/acceptlawyer")
def acceptlawyer():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM lreg where status='0'")
    data = cur.fetchall()
    #return render_template('lawyerdetails.html', data=data)
    return render_template('acceptlawyer.html',data=data)

@app.route("/court")
def court():
            return render_template('court.html')
@app.route("/lreg")
def lreg():
            return render_template('lreg.html')
@app.route("/ureg")
def ureg():
            return render_template('ureg.html')
@app.route("/search1")
def search1():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM categories")
    data = cur.fetchall()

    return render_template('userhome1.html', data=data)

     #return render_template('userhome1.html')
#-----------------------------------------------------------Admin Log Code----------------------------------------
@app.route("/adminlog", methods = ['GET', 'POST'])
def adminlog():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            error = 'Invalid Credentials. Please try again.'

            return render_template('adminhome.html')
            #return render_template('adminhome.html', error=error)
        else:
            return render_template('index.html')
@app.route("/addcat", methods = ['GET', 'POST'])
def addcat():
    error = None
    if request.method == 'POST':
        slno = request.form['slno']
        categories = request.form['categories']
        cno = request.form['cno']
        details = request.form['details']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categories VALUES ('','" + slno + "','" + categories + "','"+cno+"','"+details+"')")
        conn.commit()
        conn.close()
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        # cursor = conn.cursor()
        cur = conn1.cursor()
        cur.execute("SELECT * FROM categories")
        data = cur.fetchall()

        return render_template('adminhome.html',data=data)
@app.route("/adminhome")
def adminhome():

        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        # cursor = conn.cursor()
        cur = conn1.cursor()
        cur.execute("SELECT * FROM categories")
        data = cur.fetchall()

        return render_template('adminhome.html',data=data)


@app.route("/lawyerdetails")
def lawyerdetails():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM lreg")
    data = cur.fetchall()
    return render_template('lawyerdetails.html', data=data)
@app.route("/userdetails")
def userdetails():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM user")
    data = cur.fetchall()
    return render_template('userdetails.html', data=data)
#----------------------------------------------------------------------end admin-----------------

#----------------------------------------------------------------------lawyer module-------------------------------------
@app.route("/lawyerregister", methods = ['GET', 'POST'])
def lawyerregister():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        age = request.form['age']
        qualification = request.form['qualification']
        address=request.form['address']
        city = request.form['city']
        pnumber = request.form['pnumber']
        email = request.form['email']
        categories = request.form['specialist']
        uname = request.form['uname']
        password = request.form['password']
        f = request.files['file']
        f1 = request.files['file1']
        f.save("static/images/" + secure_filename(f.filename))
        f1.save("static/images/" + secure_filename(f1.filename))

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO lreg VALUES ('','" + name + "','" + gender + "','"+age+"','"+qualification+"','" + address + "','" + city + "','" + pnumber + "','" + email + "','" + categories + "','" + f.filename + "','"+f1.filename+"','" + uname+ "','" + password + "','0')")
        conn.commit()
        conn.close()
        return "Register Success"
@app.route("/lawyerlogin", methods = ['GET', 'POST'] )
def lawyerlogin():
    error = None
    if request.method == 'POST':
         uname = request.form['uname']
         password = request.form['password']
         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM lreg where uname='"+uname+"' and password='"+password+"'")
         data = cur.fetchone()
         if data is None:
             return 'Username or Password is wrong'
         else:
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM lreg where uname='" + uname + "' and password='" + password + "'")
            data1 = cur1.fetchall()
            for item in data1:
                 session['lname'] = item[0]
                 lid=item[0]
                 print(lid)

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')


            cur11 = conn1.cursor()
            cur11.execute("SELECT * FROM booking1 where lid='" + str(lid) + "' and status='0'")
            data11 = cur11.fetchall()
            return render_template('lawyerhome.html',data=data11)

         #return render_template('lawyerhome.html', data=data)

@app.route("/lawyerhome")
def lawyerhome():


             conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')

             lid=session['lname']
             print(lid)
             cur11 = conn1.cursor()
             cur11.execute("SELECT * FROM booking1 where lid='" + str(lid) + "' and status='0'")
             data11 = cur11.fetchall()

             return render_template('lawyerhome.html', data=data11)

@app.route("/lawyeruserdetails")
def lawyeruserdetails():


             conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')

             lid=session['lname']
             cur11 = conn1.cursor()
             cur11.execute("SELECT * FROM booking1 where lid='" + str(lid) + "' and status='Accept'")
             data4=cur11.fetchall()

             return render_template('lawyeruserdetails.html', data=data4)





@app.route("/status")
def status():


         #categories=request.form['id']
         id=request.args.get('id')
         act = request.args.get('act')
         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cursor = conn.cursor()
         cursor.execute("update booking1 set status='"+str(act)+"' where id='"+str(id)+"'")
         conn.commit()
         conn.close()
         return render_template('lawyerhome.html')
@app.route("/status1")
def status1():
    id = request.args.get('id')
    act = request.args.get('act')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    cursor = conn.cursor()
    cursor.execute("update booking1 set status='" + str(act) + "' where id='" + str(id) + "'")
    conn.commit()
    conn.close()
    return render_template('lawyerhome.html')


#-----------------------------------------------User-------------------------------------------------

@app.route("/userregister", methods = ['GET', 'POST'])
def userregister():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        address=request.form['address']
        city = request.form['city']
        pnumber = request.form['pnumber']
        email = request.form['email']
        #categories = request.form['specialist']
        uname = request.form['uname']
        password = request.form['password']
        f = request.files['file']
        f.save("static/images/" + secure_filename(f.filename))

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user VALUES ('','" + name + "','" + gender + "','" + address + "','" + pnumber + "','" + email + "','" + f.filename + "','" + uname+ "','" + password + "')")
        conn.commit()
        conn.close()
        return "Register Success"

@app.route("/userlogin", methods = ['GET', 'POST'] )
def userlogin():
    error = None
    if request.method == 'POST':
         uname = request.form['uname']
         password = request.form['password']
         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM user where uname='"+uname+"' and password='"+password+"'")
         data = cur.fetchone()
         if data is None:
             return 'Username or Password is wrong'
         else:
             cur1 = conn1.cursor()
             cur1.execute("SELECT * FROM user where uname='" + uname + "' and password='" + password + "'")
             data1=cur1.fetchall()
             for item in data1:
                 session['uname'] = item[0]

             cur2 = conn1.cursor()
             cur2.execute("SELECT * FROM categories")
             data2 = cur2.fetchall()
             print(data2)
             return render_template('userhome.html',data=data2)
         #return render_template('lawyerhome.html', data=data)

@app.route("/userhome")
def userhome():

         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM categories")
         data = cur.fetchall()
         return render_template('userhome.html',data=data)

@app.route("/search", methods=['GET','POST'])
def search():
    error = None
    if request.method == 'POST':
         categories=request.form['select']
         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM lreg where categories='"+categories+"'")
         data2 = cur.fetchall()
         cur1 = conn1.cursor()
         cur1.execute("SELECT * FROM categories")
         data = cur1.fetchall()
         return render_template('userhome1.html',data2=data2,data=data)

@app.route("/book")
def book():


         #categories=request.form['id']
         id=request.args.get('id')
         lid=str(id)
         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM lreg where id='"+lid+"'")
         d1 = cur.fetchone()
         print(d1)
         lname=d1[1]
         laddress=d1[5]
         lphone=d1[7]
         ldetails=d1[9]


         print(id)
         uid=session['uname']
         print(uid)
         conn11 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur1 = conn11.cursor()
         cur1.execute("SELECT * FROM user where id='" + str(uid) + "'")
         d11 = cur1.fetchone()
         name = d11[1]
         address = d11[3]
         phone = d11[4]
         details = d11[5]

         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cursor = conn.cursor()
         cursor.execute(
             "INSERT INTO booking1 VALUES ('','" + str(lid) + "','" + str(lname) + "','"+str(laddress)+"','"+str(lphone)+"','"+str(ldetails)+"','"+str(uid)+"','"+str(name)+"','"+str(address)+"','"+str(phone)+"','"+str(details)+"','0')")
         conn.commit()
         conn.close()
         return render_template('userhome.html')

@app.route("/lawyerbooking")
def lawyerbooking():

         uid=session['uname']
         print(uid)
         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cursor = conn.cursor()
         cursor.execute("select * from booking1 where uid='"+str(uid)+"'")
         data1 = cursor.fetchall()
         return render_template('ldetails.html',data1=data1)

@app.route("/lawyercasedetails")
def lawyercasedetails():
    lid = session['lname']
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM lreg where id='" + str(lid) + "'")
    data2 = cur.fetchall()
    for item in data2:
        name=item[1]
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM casehistory where lname='"+name+"'")
    data = cur1.fetchall()
    return render_template('lawyercasedetails.html', data=data)

@app.route("/usercasedetails")
def usercasedetails():
    lid = session['uname']
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM user where id='" + str(lid) + "'")
    data2 = cur.fetchall()
    for item in data2:
        name=item[1]
    cur1 = conn1.cursor()
    cur1.execute("SELECT * FROM casehistory where uname='"+name+"'")
    data = cur1.fetchall()
    return render_template('usercasedetails.html', data=data)
#----------------------------------------------------------court---------------------------------
@app.route("/courtlogin", methods = ['GET', 'POST'])
def courtlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            error = 'Invalid Credentials. Please try again.'
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
            # cursor = conn.cursor()
            cur = conn1.cursor()
            cur.execute("SELECT * FROM lreg")
            data2 = cur.fetchall()
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM user")
            data = cur1.fetchall()
            cur11 = conn1.cursor()
            cur11.execute("SELECT * FROM categories")
            data1 = cur11.fetchall()

            return render_template('courthome.html',data=data2,data1=data,data2=data1)
            #return render_template('adminhome.html', error=error)
        else:

            return render_template('index.html')
@app.route("/courthome")
def courthome():

            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
            # cursor = conn.cursor()
            cur = conn1.cursor()
            cur.execute("SELECT * FROM lreg")
            data2 = cur.fetchall()
            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM user")
            data = cur1.fetchall()
            cur11 = conn1.cursor()
            cur11.execute("SELECT * FROM categories")
            data1 = cur11.fetchall()

            return render_template('courthome.html',data=data2,data1=data,data2=data1)

@app.route("/addcase", methods = ['GET', 'POST'])
def addcase():
    error = None
    if request.method == 'POST':
         cno=request.form['cno'];
         status = request.form['status'];
         categories = request.form['categories'];
         uname = request.form['uname'];
         lname = request.form['lname'];
         lname1 = request.form['lname1'];
         bench = request.form['bench'];
         hdate = request.form['hdate'];
         ctitle = request.form['ctitle'];
         history = request.form['history'];
         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cursor = conn.cursor()
         cursor.execute(
                "INSERT INTO casehistory VALUES ('','" + cno + "','" + status + "','" + categories + "','" + uname + "','" + lname + "','" + lname1 + "','" + bench + "','" + hdate + "','" + ctitle + "','" + history + "')")
         conn.commit()
         conn.close()
         return "Case Added Success"

@app.route("/update")
def update():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM casehistory")
    data2 = cur.fetchall()

    return render_template('update.html',data=data2)

@app.route("/addupdate", methods = ['GET', 'POST'])
def addupdate():
    error = None
    if request.method == 'POST':
         cno=request.form['select'];
         hdate = request.form['hdate'];

         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cursor = conn.cursor()
         cursor.execute(
                "update casehistory set hdate='"+hdate+"' where cno='"+cno+"'")
         conn.commit()
         conn.close()
         return render_template('courthome.html')
@app.route("/view")
def view():
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
    # cursor = conn.cursor()
    cur = conn1.cursor()
    cur.execute("SELECT * FROM casehistory")
    data2 = cur.fetchall()

    return render_template('view.html', data=data2)
@app.route("/view1", methods = ['GET', 'POST'])
def view1():
    error = None
    if request.method == 'POST':
         cno=request.form['select'];
         #hdate = request.form['hdate'];

         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cur = conn.cursor()
         cur.execute("SELECT * FROM casehistory where cno='"+cno+"'")
         data2 = cur.fetchall()

         return render_template('view.html', data1=data2)
@app.route("/payment")
def payment():

        lid = session['uname']
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        # cursor = conn.cursor()
        cur = conn1.cursor()
        cur.execute("SELECT * FROM user where id='" + str(lid) + "'")
        data2 = cur.fetchall()
        for item in data2:
            name = item[1]
        cur1 = conn1.cursor()
        cur1.execute("SELECT * FROM casehistory where uname='" + name + "'")
        data = cur1.fetchall()
        return render_template('payment.html', data=data)

@app.route("/pay", methods=['GET','POST'])
def pay():
    error = None
    if request.method == 'POST':

         #categories=request.form['id']
         lname=request.form['select']
         accno = request.form['accno']
         amount = request.form['amount']
         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')

         uid=session['uname']
         print(uid)
         cur = conn.cursor()
         cur.execute("SELECT * FROM user where id='" + str(uid) + "'")
         data2 = cur.fetchall()
         for item in data2:
             name = item[1]

         cursor = conn.cursor()
         cursor.execute(
             "INSERT INTO pay VALUES ('','" + lname + "','" + str(name) + "','"+accno+"','"+amount+"','Card Pay')")
         conn.commit()
         conn.close()
         return render_template('userhome.html')
@app.route("/payview")
def payview():

        lid = session['uname']
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        # cursor = conn.cursor()
        cur = conn1.cursor()
        cur.execute("SELECT * FROM user where id='" + str(lid) + "'")
        data2 = cur.fetchall()
        for item in data2:
            name = item[1]
        cur1 = conn1.cursor()
        cur1.execute("SELECT * FROM pay where uname='" + name + "'")
        data = cur1.fetchall()
        return render_template('paymentview.html', data=data)
@app.route("/payview1")
def payview1():

        lid = session['lname']
        conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
        # cursor = conn.cursor()
        cur = conn1.cursor()
        cur.execute("SELECT * FROM lreg where id='" + str(lid) + "'")
        data2 = cur.fetchall()
        for item in data2:
            name = item[1]
        cur1 = conn1.cursor()
        cur1.execute("SELECT * FROM pay where lname='" + name + "'")
        data = cur1.fetchall()
        return render_template('paymentview1.html', data=data)
@app.route("/search2", methods=['GET','POST'])
def search2():
    error = None
    if request.method == 'POST':
         categories=request.form['select']
         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM categories where details='"+categories+"'")
         data = cur.fetchall()


         return render_template('userhome.html',data=data)


@app.route("/acpt")
def acpt():


         #categories=request.form['id']
         id=request.args.get('id')

         conn = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         cursor = conn.cursor()
         cursor.execute("update lreg set status='1' where id='"+str(id)+"'")
         conn.commit()
         conn.close()

         conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='ccmanagement1')
         # cursor = conn.cursor()
         cur = conn1.cursor()
         cur.execute("SELECT * FROM lreg where status='1'")
         data = cur.fetchall()

         return render_template('acceptlawyer.html',data=data)


@app.route("/dwnd")
def dwnd():


         #categories=request.form['id']
         id=request.args.get('name')
         path = 'Static/images/' + id
         return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)