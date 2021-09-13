from flask import Blueprint,make_response,redirect,request,render_template,flash,Response
from main import mongo,mail,app
import logging
from bson.objectid import ObjectId
from main.account import token_required


bp_blog = Blueprint('/blog',__name__,'/blog')

@token_required
def is_ower(id,user):
    blog = mongo.db.blog.find_one({"_id":ObjectId(id)})
    
    if not blog:
        return False
    if blog['author'] != user['_id']:
        return False
    return user



@bp_blog.route('/blog/test')
def test():
    entry = mongo.db.blog.find_one({"_id":ObjectId("6139b112987bca117e584d7b")})
    return render_template("base.html")

@bp_blog.route('/blog/create')
@token_required
def blog(user):
    if not user:
        return "Please login first"
    entry = {"title":"","content":""}
    return render_template("create.html",entry = entry)

@bp_blog.route('/blog/add',methods = ['POST','GET'])
#token or login requried
@token_required
def create_blog(user):
    if not user:
        return "please login"
    print(user)
    if request.method == "POST":
        data = request.form
        if not data or not data['title'] or not data['content'] :
            return "retry"
            
        try:
            mongo.db.blog.insert_one({
            "title":data['title'],
            "author":user['_id'],
            "content":data['content']
            })
        except:
            logging.debug("not save in database")
            return "error"
    return "done"
@bp_blog.route('/blog/edit/<string:id>')
@token_required
def edit_blog(id,user):
    blog = mongo.db.blog.find_one({"_id":ObjectId(id)})
    if not blog:
        return "Invalid id"
    if blog['author'] != user['_id']:
        return "Bad request"
    url = "/blog/edit_save/"+id
    return render_template("edit.html",entry = blog,url=url)

@bp_blog.route('/blog/edit_save/<string:id>',methods = ['POST','GET'])
def edit_save(id):
    user =  is_ower(id)
    if user == False:
        return "bad request"
    
    if request.method == "POST":
        data = request.form
        if not data or not data['title'] or not data['content']:
            return "retry"
        mongo.db.blog.update_one({"_id":ObjectId(id)}, { "$set":
            {'title':data['title'],'content':data['content']
        }})
        return "done"

    else:
        return "error"

@bp_blog.route('/blog/delete/<string:id>')
def delete_blog(id):
    user = is_ower(id) 
    if user == False:
        return "Bad request"
    try:
        mongo.db.blog.delete_one(
            {"_id":ObjectId(id)}
        )
    except:
        logging.debug("not deleted")
    return "done"
@bp_blog.route('/blog/view/<string:id>')
def view_blog(id):
    try:
        blog = mongo.db.blog.find_one(
            {"_id":ObjectId(id)}
        )
    except:
        logging.debug("not found")
        return "Bad request"
    try:
        # don't convert it for large files
        comments = list(mongo.db.comment.find(
            {"blog_id":ObjectId(id)}
        ))
    except:
        return "error"
    if not comments:
        return render_template("detail.html",entry = blog)
    else:
        for comment in comments:
            name = mongo.db.users.find_one({"_id":comment['user_id']},{"_id":0 ,  "email":0 , "password":0 , "mobile":0})
            comment['user_id'] = name['f_name'] +" " + name['l_name']
        return render_template("detail.html",entry = blog,comments = comments)

    

def view_all_blog_by_user(id):
    pass



def delete_all_blog_by_user(id):
    pass


