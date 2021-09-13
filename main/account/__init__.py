from flask import Blueprint,redirect,request,render_template,flash,make_response,jsonify
from main import mail,mongo
from flask_mail import Message
import logging
import json
import bcrypt
from functools import wraps
import jwt
from datetime import datetime, timedelta
from bson.objectid import ObjectId


bp_account = Blueprint('account',__name__,'/account',template_folder='/templetes')


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        token = request.cookies.get('token')
        #decode also check expire time automatic
        try:
            data = jwt.decode(token,"your secret key")
        except jwt.exceptions.ExpiredSignatureError:
            return "Token is expired"
        current_user = mongo.db.users.find_one({'_id':ObjectId(data['public_id'])})
        return f(user = current_user,*args,**kwargs)
    return decorated
@bp_account.route('/account/test')
@token_required
def test(current_user):
    #mes = Message(sender="vivek.v.pabari@gmail.com",recipients=["casteyekna@biyac.com","vivek.v.pabari@gmail.com"],subject="testing",body="testing")
    #mail.send(mes)
    print(current_user)
    return render_template("set_password.html")





@bp_account.route('/account/login')
def login():
    return render_template('login.html')

@bp_account.route('/account/login_verification',methods = ['POST','GET'])
def login_verification():
    if request.method == 'POST':
        data = request.form
        if not data or not data['email'] or not data['password']:
            return "Email id or/and password missing"
        else:
            #doubt CLEAR
            
            user = mongo.db.users.find_one({'email':data['email']})
            if  not user:
                return "email id not found"
            else:
                if user['password'] == data['password']:
                    #jwt or session
                    token = jwt.encode({
                        'public_id':str(user['_id']),#error when i use '_id'
                        'exp' : datetime.utcnow() + timedelta(minutes=30)
                    },"your secret key")
                    response = make_response({"token":str(token)},201)
                    response.set_cookie("token", value = token, httponly = True)
                    return response
                else:
                    
                    return "email or password is invalid"


    else:
        return "fail"
    
@bp_account.route("/account/logout")
def logout():
    response = make_response("done",201)
    response.set_cookie("token","", httponly = True)
    return response

@bp_account.route('/account/register')
def register():
    return render_template('signup.html')

@bp_account.route('/account/register_verification' , methods=['GET', 'POST'])
def register_verification():
    #check same email does not valid DONE
    if request.method == 'POST':
        data = request.form
        if not data or not data['email'] or not data['password'] or not data['f_name']  or not data['l_name'] or not data['mobile']:
            return "fail"
        else:
            user = mongo.db.users.find_one({"email":request.form['email']})
            if user:
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
        #add time in token pending
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
        response = make_response(render_template("set_password.html",token=new_token),200)
        ##response.set_cookie("reset_token",value="")
        response.headers['reset_token'] = new_token
        response.headers['email'] = data['email']
        return response

    else:
        return "Fail"
@bp_account.route('/account/password_set',methods = ['POST','GET'])
def password_set():
    if request.method == "POST":
        data = request.form
        if not data or not data['password']:
            return "Retry"
        
        #check token and return user 
        mongo.db.users.update_one({"email":user},{"$set":{"password":data['password']}})
        return "successful"
    else:
        return "Error"




