'''
Registration of user
Each use get 10 points
Store a sentance on our database for1 tocken
Retrive his stored sentance on out database for 1 token
'''
from flask import Flask,jsonify,request
from flask_restful import Api,Resource
import os
from pymongo import MongoClient
import bcrypt
app=Flask(__name__)
api=Api(app)
client=MongoClient("mongodb://db:27017")
#above db is name in name in docker-compose.yml
#create database of name SentencesDatabse and object to that database is db
db=client.SentencesDatabase
#create collection
users=db['Users']
#register with user name and password
class Register(Resource):
    def post(self):
        #get the posted data by user
        postedData=request.get_json()
        #get data
        username=postedData['username']
        password=postedData['password']
        #hash(password+salt)=kjoaioaw3o488fo
        #password=password.encode()
        hashed_pw=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        #store user name and password in data base
        users.insert_one({
         "Username":username,
         "Password":hashed_pw,
         "Sentance":'',
         "Tokens": 6
        })
        retJson={
        "status":200,
        "msg":'You are succfully signed uo for API'
        }
        return jsonify(retJson)
def verifyPw(username,password):
    hashed_pw=users.find({
    "Username":username
    })[0]['Password']
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
    #return bcrypt.checkpw(password.encode(),hashed_pw)
def countTokens(username):
    tokens=users.find({
    'Username':username
        })[0]['Tokens']
    return tokens
class Store(Resource):
    def post():
        #get posted data
        postedData=request.get_json()
        #read hte data
        username=postedData['username']
        password=postedData['password']
        sentance=postedData['sentance']
        #verify user name and password
        correct_pw=verifyPw(username,password)
        if not correct_pw:
            retJson={
            'status':302
            }
            return jsonify(retJson)
        #count number of tokens
        num_tokens=countTokens(username)
        if num_tokens<=0:
            retJson={
            'status':301
            }
            return jsonify(retJson)
        #store the sentance and take one token away
        users.update({
        "Username":username
        },{
        '$set':{
        'Sentance':sentance,'Tokens':num_tokens-1
        }
        })
        retJson= {
        'status':200,
        'msg':"sentence saved sucefully"
        }
        return jsonify(retJson)
class Get(Resource):
    def get(self):
        postedData=request.get_json()
        #read hte data
        username=postedData['username']
        password=postedData['password']
        #verify user name and password
        correct_pw=verifyPw(username,password)
        if not correct_pw:
            retJson={
            'status':302
            }
            return jsonify(retJson)
        #count number of tokens
        num_tokens=countTokens(username)
        if num_tokens<=0:
            retJson={
            'status':301
            }
            return jsonify(retJson)
        sentance=users.find({
        "Username":username
        })[0]["Sentance"]
        retJson={
         "status":300,
         "Sentance":sentance
        }
        return jsonify(retJson)

@app.route('/')
def hello():
    retJson={
    'name':'naresh',
    'no':97050
    }
    return jsonify(retJson)

api.add_resource(Register,'/register')

api.add_resource(Store,'/store')
adi.add_resource(Get,"/get")
if __name__=='__main__':
    app.run(host="0.0.0.0")



'''
from flask import Flask,jsonify,request
from flask_restful import Api,Resource
import os
from pymongo import MongoClient
app=Flask(__name__)
api=Api(app)
client=MongoClient("mongodb://db:27017")
db=client.aNewDB   #create data base now we can call with aNewDB
UserNum=db['UserNum']  #creating collection UserNum
#create a document in collection
#find number of user visit we site
UserNum.insert({
'num_of_users':0
})
class Visit(Resource):
    #get previus number from collection and updat
    def get(self):
         prev_num=UserNum.find({})[0]['num_of_users']
         new_num=prev_num+1
         UserNum.update({},{"$set":{"num_of_users":new_num}})
         return str('hello user :'+str(new_num))
def cheakpostd_data(post,fun):
    if(fun=='add'):
        if 'x' not in post or 'y' not in post:
            return 301
        else :
            return 200
class Add(Resource):
    def post(self):
        postdata=request.get_json()
        status_code=cheakpostd_data(postdata,'add')
        if(status_code!=200):
            refjson={"Massage":"Error is happen",
            'status_code':status_code
            }
            return jsonify(refjson)
        else:
            x=postdata["x"]
            y=postdata["y"]
            z=x+y
            data={
            "z":z
            }
            return jsonify(data)
@app.route('/')
def hello():
    return 'hello world'
api.add_resource(Add,'/add')
api.add_resource(Visit,'/hello')
if __name__=='__main__':
    app.run(host="0.0.0.0")
'''
