"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/add_member',methods=['POST'])
def add_member():
    try:
        member=dict()
        member["id"]=jackson_family._generateId()
        member["first_name"]= request.json.get("first_name")
        member["last_name"]=jackson_family.last_name 
        member["age"]= int(request.json.get("age"))
        member["Lucky_numbers"]= request.json.get("lucky_numbers")
        print(member)
        return jsonify(jackson_family.add_member(member)),200
    except Exception as e:
        return jsonify("Bad Request"),400
    
@app.route('/delete_member/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        member=jackson_family.delete_member(int(id))
        if member!=None:
            return jsonify({"msg":"Member Delete"}),200
        else:
            return jsonify({"msg":"not found"}),404
    except Exception as e:
        return jsonify({"msg":"Bad request"}),400

@app.route('/member/<int:id>')
def get_member(id):
    try:
        member=jackson_family.get_member(int(id))
        if member!= None:
            return jsonify({"member":member}),200
        else:
            return jsonify({"msg":"not found"}),404
    except Exception as e:
        return jsonify({"Msg":e}),400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
