import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  '''
  @TODO: Done Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={'/': {'origins': '*'}})
  '''
  @TODO:Done Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods','GET,PUT,POST,DELETE,OPTIONS')
    return response
  '''
  @TODO: Done
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():
    #get all the categories from the db
    Categories = Category.query.all()
    #format the categories
    formatted_categories = [category.format() for category in Categories]
    #to format it in the shape of "type" : "id"
    final_answer={}
    for i in range (0,len(formatted_categories)):
      final_answer[formatted_categories[i]['id']]=formatted_categories[i]['type']
    return jsonify({
      'categories': final_answer,
    })

  '''
  @TODO:Done
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: Done At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
    page = request.args.get('page',1,type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    #get all questions from the database
    Questions = Question.query.all()
    #check that there are questions and it is not empty
    if (len(Questions) == 0):
      abort(404)
    #calculating the end will depend on the number of questions left.
    if len(Questions)-start >= 10:
      end = start + QUESTIONS_PER_PAGE
    else:
      end = start + (len(Questions)-start)
    #format all the questions
    formatted_questions = [question.format() for question in Questions]

    #getting the current categories of the questions shown not all the questions 
    final_answer2 = []
    for i in range (start,end):
      final_answer2.append(formatted_questions[i]['category']) 
    
    #getting all the categories
    Categories = Category.query.all()
    formatted_categories = [category.format() for category in Categories]

    #getting the catgories in the shape of "id":"type" 
    final_answer1={}
    for i in range (0,len(formatted_categories)):
      final_answer1[formatted_categories[i]['id']]=formatted_categories[i]['type']
    
    #check that the questions from start to end are not empty
    if len(formatted_questions[start:end]) == 0:
      abort(404)
    return jsonify({
      'categories': final_answer1,
      'current_category': final_answer2,
      'questions' : formatted_questions[start:end],
      'total_questions': len(formatted_questions),
      'success' : True
    })

  '''
  @TODO: Done
  Create an endpoint to DELETE question using a question ID. 

  TEST: Done When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
    try:
      #get the question with the id given
      question = Question.query.filter(Question.id == question_id).one_or_none()
      #if it is not there abort 
      if question is None:
        abort(404)
      #delete the question
      question.delete()
      
      #doing exactly the same thing again like we are getting questions
      #### like get question end point
      page = request.args.get('page',1,type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      #get all questions from the database
      Questions = Question.query.all()
      #check that there are questions and it is not empty
      if (len(Questions) == 0):
        abort(404)
      #calculating the end will depend on the number of questions left.
      if len(Questions)-start >= 10:
        end = start + QUESTIONS_PER_PAGE
      else:
        end = start + (len(Questions)-start)
      #format all the questions
      formatted_questions = [question.format() for question in Questions]

      #getting the current categories of the questions shown not all the questions 
      final_answer2 = []
      for i in range (start,end):
        final_answer2.append(formatted_questions[i]['category']) 
      
      #getting all the categories
      Categories = Category.query.all()
      formatted_categories = [category.format() for category in Categories]

      #getting the catgories in the shape of "id":"type" 
      final_answer1={}
      for i in range (0,len(formatted_categories)):
        final_answer1[formatted_categories[i]['id']]=formatted_categories[i]['type']
      
      #check that the questions from start to end are not empty
      if len(formatted_questions[start:end]) == 0:
        abort(404)

      return jsonify({
        'categories': final_answer1,
        'current_category': final_answer2,
        'questions' : formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'success' : True
      })
    except:
      abort(422)


  '''
  @TODO: Done 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: Done When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions',methods=['POST'])
  def create_question():
    #get the body of the request
    body = request.get_json()

    #get the required data to create new question in the database
    new_question = body.get('question',None)
    new_answer = body.get('answer',None)
    new_category = body.get('category',None)
    new_score = body.get('difficulty',None)

    try:
      #creating the new question
      question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_score)
      #inserting the question in the database
      question.insert()
      
      #doing exactly the same thing again like we are getting questions
      #### like get question end point
      page = request.args.get('page',1,type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      #get all questions from the database
      Questions = Question.query.all()
      #check that there are questions and it is not empty
      if (len(Questions) == 0):
        abort(404)
      #calculating the end will depend on the number of questions left.
      if len(Questions)-start >= 10:
        end = start + QUESTIONS_PER_PAGE
      else:
        end = start + (len(Questions)-start)
      #format all the questions
      formatted_questions = [question.format() for question in Questions]

      #getting the current categories of the questions shown not all the questions 
      final_answer2 = []
      for i in range (start,end):
        final_answer2.append(formatted_questions[i]['category']) 
      
      #getting all the categories
      Categories = Category.query.all()
      formatted_categories = [category.format() for category in Categories]

      #getting the catgories in the shape of "id":"type" 
      final_answer1={}
      for i in range (0,len(formatted_categories)):
        final_answer1[formatted_categories[i]['id']]=formatted_categories[i]['type']
      
      #check that the questions from start to end are not empty
      if len(formatted_questions[start:end]) == 0:
        abort(404)

      return jsonify({
        'categories': final_answer1,
        'current_category': final_answer2,
        'questions' : formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'success' : True
      })
    except:
      abort(405)


  '''
  @TODO: Done
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Done Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search',methods=['POST'])
  def search_question():
    try:
      #get the body of the request
      body = request.get_json()
      #getting the searchTerm from the request body
      searchTerm = body.get('searchTerm',None)

      #abort if the searchterm is none
      if searchTerm is None:
        abort(404)
      
      #getting all the questions from the database
      Questions = Question.query.all()
      #format the questions
      formatted_questions = [question.format() for question in Questions]
      #getting the questions that the searchTerm is substring of
      search_questions = Question.query.filter(Question.question.ilike(f'%{searchTerm}%')).all()
      currentCategory = []
      #getting the categories of the questions chosen
      for i in range (0,len(search_questions)):
        currentCategory.append(search_questions[i]['category']) 

      return jsonify({
        'questions': search_questions,
        'current_category': currentCategory,
        'total_questions': len(formatted_questions),
        'success' : True
        })
    except:
      abort(400)
    

  '''
  @TODO: Done
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions',methods=['GET'])
  def get_question_by_category(category_id):
    try:
      #checking that the category_id is available in the database
      id = Category.query.filter(Category.id == category_id).one_or_none()
      if id is None:
        abort(404)
      #getting all the questions from the database     
      Questions = Question.query.all()
      formatted_questions = [question.format() for question in Questions]
      final_answer = []
      #getting the questions related to this category_id
      for i in range (0,len(formatted_questions)):
        if (formatted_questions[i]['category']==category_id):
          final_answer.append(formatted_questions[i])
      return jsonify({
        "questions" : final_answer,
        "total_questions" : len(formatted_questions),
        "current_category" : category_id,
        "success" : True
      })
    except:
      abort(422)


  '''
  @TODO: Done
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: Done In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def play_quiz():
    #get the body of the request
    body = request.get_json()

    #getting the needed info from the body of the request
    previousQuestions = body.get('previous_questions')
    category = body.get('quiz_category')

    #checking that there is category and prevquestions
    if ((category is None ) or (previousQuestions is None)):
      abort(400)
    #getting the category_id
    category_id = int(category['id'])
    
    #checking if the user selected All or one of the types
    if(category_id == 0):
      Questions = Question.query.all()
    else:
      Questions = Question.query.filter_by(category=category_id).all()
    
    #getting the number of questions
    total_questions = len(Questions)
    
    #function to check if the questions is used before to ignore it 
    def check_if_used(question):
      used = False
      for que in previousQuestions:
        if (que == question.id):
          used = True
      return used
    
    #getting a random question from the selected questions
    question = Questions[random.randrange(0,len(Questions),1)]
    
    #checking the question and if the game ended
    while(check_if_used(question)):
      question = Questions[random.randrange(0,len(Questions),1)]
      if (len(previousQuestions) == total_questions):
        print("Here")
        return jsonify({
          'success': True
        })


    return jsonify({
      'question' : question.format(),
      'success' : True
    })    

  '''
  @TODO: Done 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error" : 404,
      "message" : "resource not found"
    }),404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "error" : 422,
      "message" : "unprocessable"
    }),422

  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message" : "bad request"
    }),400

  @app.errorhandler(405)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "error" : 405,
      "message" : "method not allowed"
    }),405
  
  return app

    