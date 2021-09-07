#library 

from flask import Flask,redirect,request,render_template,session,jsonify

from flask import Flask

from database.setup import mongo,mail

from functools import wraps

import jwt


app = Flask(__name__)
app.config['secret_key'] = "5de28bb0b0ba249162870c676df13ce5"
app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vivek.v.pabari@gmail.com'
app.config['MAIL_PASSWORD'] = 'shopno.46'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mongo.init_app(app)
mail.init_app(app)



#register blueprints
from account import temp
from blog import code
app.register_blueprint(temp.bp_account)
app.register_blueprint(code.bp_blog)

from flask_mail import Mail,Message
"""

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        print(request.headers['x-access-token'])
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return "Token is missing"
        try:
            data = jwt.decode(token,"your secret key")
            current_user = mongo.db.users.find_one({'_id':data['public_id']})

        except:
            return "Token is invalid"
        return f(current_user,*args,**kwargs)
    return decorated
""" 

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           current_user = Users.query.filter_by(public_id=data['public_id']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator

@app.route('/test')
@token_required
def test(current_user):
    #mes = Message(sender="vivek.v.pabari@gmail.com",recipients=["casteyekna@biyac.com","vivek.v.pabari@gmail.com"],subject="testing",body="testing")
    #mail.send(mes)
    print(current_user)
    return "pass"



@app.route('/')
def index():
    user = mongo.db.users.find_one({"email":"v"})
    return user['f_name']

if __name__ == "__main__":
    app.run(debug=True)

