import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO-Done- implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
#public so no need for authorization or permissions
@app.route('/drinks')
def get_drinks():
    all_drinks = Drink.query.all() #get all the drinks from the database
    drinks = [drink.short() for drink in all_drinks] #format it in the short form
    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200



'''
@TODO-Done- implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    all_drinks = Drink.query.all() #get all the drinks from the database
    drinks = [drink.long() for drink in all_drinks] #format it in the long form
    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200

'''
@TODO-Done- implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks',methods=['POST'])
@requires_auth('post:drinks')
def post_new_drink(jwt):
    post_request = request.get_json() #to access the post parameters and take the desired values
    try:
        drink = Drink() #make an instance from the Drink class 
        drink.title = post_request['title']
        post_request_recipe = post_request['recipe']
        if isinstance(post_request_recipe,dict): #check if the recipe is a dict
            post_request_recipe = [post_request_recipe ] #turn it into list
        drink.recipe = json.dumps(post_request_recipe) #to turn it into a string as classified in the models.py
        drink.insert() #insert the new row into the database
    except BaseException:
        abort(400)
    drinks = [drink.long()] #array containing the newly added drink

    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200

'''
@TODO-Done- implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(jwt,id):
    patch_request = request.get_json()  #to access the request parameters and take the desired values
    drink = Drink.query.filter(Drink.id == id).one_or_none() #get the drink from the database
    if not drink: #if the drink wasnot in the database
        abort(404)
    try:
        patch_req_title = patch_request.get('title')
        patch_req_recipe = patch_request.get('recipe')

        if patch_req_title:
            drink.recipe = patch_req_title

        if patch_req_recipe:
            drink.recipe = json.dumps(req['recipe'])

        drink.update() #update the existing rowdrink
        print(drink.recipe)
        print(drink.title)
        print(drink.id)
        drink.recipe = json.dumps(drink.recipe )
        drinks = [drink.long()]  #array containing the newly updated drink

    except BaseException:
        abort(400)

    return jsonify({
        "success" : True,
        "drinks" : drinks
    }), 200

'''
@TODO-Done- implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>',methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt,id):
    drink = Drink.query.filter(Drink.id == id).one_or_none() #get the drink from the database
    if not drink: #if the drink wasnot in the database
        abort(404)
    try:
        drink.delete() #delete the desired drink from the db
    except BaseException:
        abort(400)

    return jsonify({
        "success" : True,
        "delete" : id
    }), 200

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO-Done- implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO-Done- implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(422)
def notfound(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@TODO-Done- implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def AuthError(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code