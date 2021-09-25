from main import mongo,mail,app
import logging
import json
from bson.objectid import ObjectId
from main.account import token_required
from flask_restful import Resource
from flask import Flask,redirect,request,render_template,session,jsonify,Response,make_response
import jwt
from datetime import datetime,timedelta


class SignupApi(Resource):
    def post(self):
        try:
            data = request.get_json()
            mongo.db.users.insert_one(
                {
                    "f_name":data['f_name'],
                    "l_name":data['l_name'],
                    "email":data['email'],
                    "password":data['email'],
                    "number":data['number']
                }
            )
            return "Added",200
        except:
            return "Error"


class LoginApi(Resource):
    def post(self):
        data = request.get_json()
        if not data or not data['email'] or not data['password']:
            return "retry"
        user = mongo.db.users.find_one({"email":data["email"]})
        
        if not user:
            return "Email Not Found"
        if user['password'] != data['password']:
            return "Invalid Email or password"
        token = jwt.encode({
                    'public_id':str(user['_id']),#error when i use '_id'
                    'exp' : datetime.utcnow() + timedelta(minutes=30)
                },"your secret key")
        response = make_response({"token":str(token)},201)
        response.set_cookie("token", value = token, httponly = True)
        return response
