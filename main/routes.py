from main import app,mongo
from flask import render_template


@app.route('/')
def index():
    li =  mongo.db.blog.find()
    return render_template("index.html",object_list = li)
