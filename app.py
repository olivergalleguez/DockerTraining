from flask import Flask, redirect, url_for, \
				  request, render_template, json
from pymongo import MongoClient
import pymongo
import os
import socket
from bson import ObjectId



class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient('mongodb://backend:1234/dockerdemo')
db = client.blogpostDB

app = Flask(__name__)

@app.route("/")
def landing_page():
    posts = get_all_posts()
    
    return render_template('blog.html', posts=json.loads(posts))


@app.route('/add_post', methods=['POST'])
def add_post():

    new()
    return redirect(url_for('landing_page'))


@app.route('/remove_all')
def remove_all():
    db.blogpostDB.delete_many({})

    return redirect(url_for('landing_page'))




## Services

@app.route("/posts", methods=['GET'])
def get_all_posts():
    
    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]
    return JSONEncoder().encode(posts)

@app.route("/posts/<id>", methods=['GET'])
def get_post_by_id(id):
    
    post = db.blogpostDB.find_one({"_id": ObjectId(id)})
    return JSONEncoder().encode(post)

@app.route("/posts/<id>", methods=['DELETE'])
def delete_post_by_id(id):
    
    post = db.blogpostDB.delete_one({"_id": ObjectId(id)})
    return "true"

@app.route("/posts/<id>", methods=['PUT'])
def edit_post(id):    
    data = request.get_json()
    print("request data")
    print(data['post']);
    
    post = db.blogpostDB.find_one({"_id": ObjectId(id)})
    db.blogpostDB.update_one(
        {"_id": ObjectId(id)}, 
        {
            "$set" : {
                'title': data['title'],
                'post': data['post']
             }
        }
    )
    post = db.blogpostDB.find_one({"_id": ObjectId(id)})
    return JSONEncoder().encode(post)


@app.route('/new', methods=['POST'])
def new():

    item_doc = {
        'title': request.form['title'],
        'post': request.form['post']
    }
    db.blogpostDB.insert_one(item_doc)

    _posts = db.blogpostDB.find()
    posts = [post for post in _posts]

    return JSONEncoder().encode(posts[-1])


### Insert function here ###



############################



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
