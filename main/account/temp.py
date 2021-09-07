from flask import Blueprint,redirect,request,render_template,flash,make_response,jsonify
from database.setup import mongo,mail
from flask_mail import Message
import logging
import json
import bcrypt
from functools import wraps
import jwt
from datetime import datetime, timedelta


bp_account = Blueprint('account',__name__,'/account')


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        token = request.cookies.get('token')
        print(token)
        data = jwt.decode(token,"your secret key")
        current_user = mongo.db.users.find_one({'email':data['public_id']})
        return f(current_user,*args,**kwargs)
    return decorated
@bp_account.route('/account/test')
@token_required
def test(current_user):
    #mes = Message(sender="vivek.v.pabari@gmail.com",recipients=["casteyekna@biyac.com","vivek.v.pabari@gmail.com"],subject="testing",body="testing")
    #mail.send(mes)
    print(current_user)
    return "pass"

""" def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(public_id = data['public_id'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated
    # route for logging user in
@app.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.form
  
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
  
    user = User.query\
        .filter_by(email = auth.get('email'))\
        .first()
  
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
  
    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'public_id': user.public_id,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, app.config['SECRET_KEY'])
  
        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )
  
    
    """



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
            #doubt 
            
            user = mongo.db.users.find_one({'email':data['email']})
            if  not user:
                return "email id not found"
            else:
                if user['password'] == data['password']:
                    #jwt or session
                    token = jwt.encode({
                        'public_id':user['email'],#error  
                        'exp' : datetime.utcnow() + timedelta(minutes=30)
                    },"your secret key")
                    response = make_response({"token":token},201)
                    response.headers['token'] = token
                    response.set_cookie("token", value = token, httponly = True)
                    response.headers['X-Parachutes'] = 'parachutes are cool'
                    return response
                else:
                    print(type(user['password']),type(data['password']))
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

    




