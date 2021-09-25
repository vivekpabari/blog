from main import mongo,mail,app
import logging
import json
from bson.objectid import ObjectId
from main.account import token_required
from flask_restful import Resource
from flask import Flask,redirect,request,render_template,session,jsonify,Response
from main.blog.code import is_ower

class blogadd(Resource):
    @token_required
    def post(self,user):
        data = request.get_json()
        mongo.db.blog.insert_one({
        "title":data['title'],
        "author":ObjectId(user['_id']),
        "content":data['content']
        }) 
        return "uploaded", 200

class blogApi(Resource):
    def put(self,id):
        blog = mongo.db.blog.find_one({"_id":ObjectId(id)})
        if not blog:
            return "Blog does not exits"
        user = is_ower(id) 
        if user == False:
            return "Invalid"
        data = request.get_json()
        mongo.db.blog.update_one({"_id":ObjectId(id)}, { "$set":
            {'title':data['title'],'content':data['content']
        }})
        return "updated", 200
        

              

    
    def delete(self, id):
        user = is_ower(id) 
        if user == False:
            return "Invalid"
        try:
            blog = mongo.db.blog.delete_one({"_id":ObjectId(id)})
            return 'Done', 200
        except:
            return "error"

    
    def get(self,id):
        blog = mongo.db.blog.find_one({"_id":ObjectId(id)},{"_id":0,"author":0})
        if not blog:
            return "Blog Not Present" 
        return jsonify(blog)
