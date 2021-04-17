import os
import unittest
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # Create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"*/api/*": {origins: '*'}})

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''

  @app.route('/categories', methods=['GET'])
  def get_categories():
    ''' Retrieve dictionary of categories'''
    try:
      categories = Category.query.order_by(Category.id).all()
      return jsonify({
        'success': True,
        'categories': {
          category.id: category.type for category in categories
        }
      })
    except:
      abort(422
      )

  @app.route('/questions', methods=['GET'])
  def get_questions():
    ''' Retrieve questions. Paginate results. '''
    try:
      page = request.args.get('page', 1, type=int)
      
      questions = Question.query.order_by(Question.id) \
        .paginate(page=page, per_page=QUESTIONS_PER_PAGE)
      
      questions_formatted = [ 
        question.format() for question in questions.items
        ]

      categories = Category.query.order_by(Category.id).all()
      
      categories_formatted = {
        category.id: category.type for category in category
      }

      if len(questions_formatted) == 0:
        abort(404)
      else:
        return jsonify({
          'success': True,
          'questions': questions_formatted,
          'total_questions': questions.total,
          'categories': category_formatted,
          'current_category': None 
        })
    except Exception as e:
      if  '404' in str(e):
        abort(404)
      else:
        abort(422)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    ''' Retrieve questions based on category. '''
    try:
      page = request.args.get('page', 1, type=int)

      questions = Questions.query.order_by(Question.id) \
        .filter(Questions.category == category_id) \
        .paginate(page=page, per_page=QUESTIONS_PER_PAGE)

      questions_formatted = [
        question.format() for question in questions.items
      ]

      if len(questions_formatted) == 0:
        abort(404)
      else:
        return jsonify({
          'success': True,
          'questions': questions_formatted,
          'total_questions': questions.total,
          'current_category': category_id
        })
    except Exception as e:
      if '404' in str(e):
        abort(404)
      else:
        abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app
    