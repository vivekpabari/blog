from flask import Blueprint,redirect,request,render_template,flash
from database.setup import mongo,mail
from flask_mail import Message
import logging
import json
import bcrypt


bp_account = Blueprint('account',__name__,'/account')




@bp_account.route('/account/test')
def test():
    mes = Message(sender="vivek.v.pabari@gmail.com",recipients=["vivek.v.pabari@gmail.com"],subject="testing123",body="testing")
    mail.send(mes)
    return "pass"

@bp_account.route('/account/login')
def login():
    return render_template('login.html')

@bp_account.route('/account/login_verification',methods = ['POST','GET'])
def login_verification():
    if request.method == 'POST':
        if not request.form['email'] or not request.form['password']:
            return "fail"
        else:
            #doubt 
            user = mongo.db.users.find_one({'email':request.form['email']})
            if  user == None:
                return "email id not found"
            else:
                if user['password'] == request.form['password']:
                    #jwt or session
                    return redirect('/')
                else:
                    return "email or password is invalid"


    else:
        return "fail"
    

def logout():
    pass

@bp_account.route('/account/register')
def register():
    return render_template('signup.html')

@bp_account.route('/account/register_verification' , methods=['GET', 'POST'])
def register_verification():
    #check same email does not valid
    if request.method == 'POST':
        print("hii")
        if not request.form['email'] or not request.form['password'] or not request.form['f_name']  or not request.form['l_name'] or not request.form['mobile']:
            return "fail"
        else:
            user = mongo.db.users.find_one({"email":request.form['email']})
            if user != None:
                return "email already register"
            else:
                try:
                    mongo.db.users.insert_one({
                        "f_name":request.form['f_name'],
                        "l_name":request.form['l_name'],
                        "email": request.form['email'],
                        "password":request.form['password'],
                        "mobile":request.form['mobile']
                    })
                except:
                    logging.error("not save in database")
                return "pass"

    else:
        return "fail"






@bp_account.route('/account/forget_password')
def forget_password():
    return render_template('forget.html')


@bp_account.route('/account/send_one_time_link',methods = ['POST','GET'])
def sending_mail():
    #checking email exit or not
    if request.method == 'POST':
        data = request.form
        if not data or not data['email']:
            return "fail"
        user = mongo.db.user.find_one({"email":data['email']})
        print(user)
        token = bcrypt.hashpw(data['email'].encode('utf-8'),b'$2b$12$T5mTP49XpLT1cRGp.noVoe')
        url = "http://127.0.0.1:5000/account/resetpassword?email="+data['email']+"&token="+token.decode()
        mes = Message(sender="vivek.v.pabari@gmail.com",recipients=[data['email']],subject="reset password",body=url)
        mail.send(mes)
        return "Click on link given to you"
    else:
        return "fail"

@bp_account.route('/account/resetpassword',methods = ['POST','GET'])
def resetpassword():
    if request.method == 'GET':
        data = request.args
        if not data or not data['email'] or not data['token']:
            return "fail"
        new_token = bcrypt.hashpw(data['email'].encode('utf-8'),b'$2b$12$T5mTP49XpLT1cRGp.noVoe').decode()
        if new_token!=data['token']:
            return "retry"
        try:
            mongo.db.users.find_one_and_update({"email":"v"},{'password':"new psa"})
        except:
            return "error"

    else:
        return "Fail"

    




