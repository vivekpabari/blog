from flask import Blueprint,redirect,request,render_template,flash
from main import mongo,mail
import logging

bp_blog = Blueprint('blog',__name__,'/blog')

@bp_blog.route('/blog/test')
def test():
    return "pass"

"""
def create_blog(data):
    try:
        mongo.db.blog.insert_one({
        "title":data[title],
        "author":data[author],
        "content":data[content],
        "likes":data[likes]
        })
    except:
        logging.debug("not save in database")
def edit_blog():
    pass

@bp_blog.route('/blog/delete/<int:id>')
def delete_blog(id):
    #check if he is owner of blog
    try:
        mongo.db.blog.delete_one(
            {"_id":id}
        )
    except:
        logging.debug("not deleted")
    return "done"
@bp_blog.route('blog/<int:id>')
def view_blog(id):
    try:
        blog = mongo.db.blog.find_one(
            {"_id":id}
        )
    except:
        logging.debug("not found")
    return "done"

    
"""
def view_all_blog_by_user(id):
    pass



def delete_all_blog_by_user(id):
    pass