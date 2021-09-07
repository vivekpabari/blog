#library 

from flask import Flask,redirect,request,render_template,session,jsonify

from flask import Flask

from database.setup import mongo,mail



app = Flask(__name__)
app.config['sceret_key'] = "5de28bb0b0ba249162870c676df13ce5"
app.config["MONGO_URI"] = "mongodb://localhost:27017/blog"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vivek.v.pabari@gmail.com'
app.config['MAIL_PASSWORD'] = 'xyz'
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




@app.route('/test')
def test():
    mes = Message(sender="vivek.v.pabari@gmail.com",recipients=["casteyekna@biyac.com","vivek.v.pabari@gmail.com"],subject="testing",body="testing")
    mail.send(mes)
    return "pass"

@app.route('/')
def index():
    return "Do Your Best"

if __name__ == "__main__":
    app.run(debug=True)

