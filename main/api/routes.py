from flask import Flask,redirect,request,render_template,session,jsonify
import json
from flask_restful import Resource
from main import API


from .account import SignupApi,LoginApi

#from .reset_password import ForgotPassword, ResetPassword

from .blog import blogApi,blogadd

def initialize_routes():
    API.add_resource(blogadd, '/api/blog/add')
    API.add_resource(blogApi, '/api/blog/<id>')
    
    API.add_resource(SignupApi, '/api/account/signup')
    API.add_resource(LoginApi, '/api/account/login')
    



