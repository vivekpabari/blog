from flask_mail import Mail,Message
from main_app import app
import password
from main.database.setup import mail


def config_mail():
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'vivek.v.pabari@gmail.com'
    app.config['MAIL_PASSWORD'] = fjhyt
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    
    
def sending_mail(sender_id,reciver_id,subject_,body_):
    message = Message(subject=testing,recipients=reciver_id,body=body_,sender=sender_id)
    mail.sent(message)
