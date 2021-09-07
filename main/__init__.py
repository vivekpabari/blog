#library 

from flask import Flask,redirect,request,render_template,session,jsonify

from flask import Flask



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

from flask_pymongo import PyMongo
mongo = PyMongo(app)


from flask_mail import Mail,Message
mail = Mail(app)


#routes
from main import routes


#register blueprints
from main import account
from main.blog import code
app.register_blueprint(account.bp_account)
app.register_blueprint(code.bp_blog)




