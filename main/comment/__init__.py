from flask import Blueprint,redirect,request,render_template,flash,make_response,jsonify
from main import mongo
from main.account import token_required
from bson.objectid import ObjectId
bp_comment = Blueprint("comment",__name__)


@bp_comment.route("/comment/add",methods=["POST","GET"])
@token_required
def comment_add(user):
    if not user:
        return "please to login"
    if request.method == "POST":
        data = request.form
    
        if not data or not data['content'] or not data['blog_id']:
            return "Retry"
        try:
            mongo.db.comment.insert_one({
                "user_id":user['_id'],
                "blog_id":ObjectId(data['blog_id']),
                "content":data['content']
            })
        except:
            return "error"

        #how to return to same page
        return "Done"
    else:
        return "error"



            
