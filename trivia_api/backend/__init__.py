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

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    ''' Delete question using question_id. '''
    try:
      question = Question.query.filter(Question.id == question_id) \
        .one_or_none()

      if question is None:
        abort(404)

      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })
    
    except Exception as e:
      if '404' in str(e):
        abort(404)
      else:
        abort(422)

  @app.route('/questions', methods=['POST'])
  def new_question():
    ''' Add a new question. '''
    body = reqeust.get_json()
    question = body.get('question', None)
    answer = body.get('answer', None)
    difficulty = body.get('difficulty', None)
    category = body.get('category', None)

    try:
      question = Question(
        question=question,
        answer=answer,
        difficulty=difficulty,
        category=category
      )

      question.insert()

      return jsonify({
        'success': True,
        'created': question.id
      })
    
    except Exception:
      abort(422)

  '''@TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app_route('/search', methods=['POST'])
  def search_question():
    ''' Search questions based on a term. '''
  body = request.get_json()
  search = body.get('searchTerm', None)

  try:
    question = Question.query.order_by(Question.id) \
      .filter(Question.question.ilike('%{}%'.format(search)))

    questions_formatted = [
      question.format() for question in questions
    ]

    return jsonify({
      'success': True,
      'questions': questions_formatted,
      'total_questions': len(questions.all()),
      'current_category': None
    })
  except Exception:
    abort(422)

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
    