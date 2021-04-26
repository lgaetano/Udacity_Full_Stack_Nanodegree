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
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # CORS Headers
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return response

  @app.route('/categories', methods=['GET'])
  def get_categories():
    ''' Retrieve dictionary of categories'''

    try:
      # Retrieve all categories
      categories = Category.query.order_by(Category.id).all()

      return jsonify({
        'success': True,
        'categories': {
          category.id: category.type for category in categories
        }
      })

    except:
      abort(422)

  @app.route('/questions', methods=['GET'])
  def get_questions():
    ''' Retrieve questions. Paginate results. '''

    try:
      # Get page
      page = request.args.get('page', 1, type=int)
      
      # Query, paginate and format questions
      questions = Question.query.order_by(Question.id) \
        .paginate(page=page, per_page=QUESTIONS_PER_PAGE)
      
      questions_formatted = [ 
        question.format() for question in questions.items
        ]

      # Query and format categories
      categories = Category.query.order_by(Category.id).all()
      
      categories_formatted = {
        category.id: category.type for category in categories
      }

      if len(questions_formatted) == 0:
        abort(404)
      else:
        return jsonify({
          'success': True,
          'questions': questions_formatted,
          'total_questions': questions.total,
          'categories': categories_formatted,
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

    # Query for question with id == question_id
    question = Question.query.get(question_id)

    if question is None:
      abort(404)

    try:
      # Delete question from database
      question.delete()

    except Exception as e:
      abort(422)

    else:
      return jsonify({
        'success': True,
        'deleted': question_id
      })

  @app.route('/questions', methods=['POST'])
  def new_question():
    ''' Add a new question. '''

    # Retrieve raw data
    data = request.get_json()
    question = data.get('question', None)
    answer = data.get('answer', None)
    difficulty = data.get('difficulty', None)
    category = data.get('category', None)

    try:
      # Create a question
      question = Question(
        question=question,
        answer=answer,
        difficulty=difficulty,
        category=category
      )

      # Update the database
      question.insert()

      return jsonify({
        'success': True,
        'created': question.id
      })
    
    except Exception:
      print('Exception raised >> ' , e)
      abort(422)

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    ''' Search questions based on a term. '''
  
    # Retrieve raw data
    data = request.get_json()
    search_term = data.get('searchTerm', None)

    try:
      # Query for search term and format
      if search_term:
        questions = Question.query.order_by(Question.id) \
          .filter(Question.question.ilike('%{}%'.format(search_term))).all()

        questions_formatted = [
          question.format() for question in questions
        ]

        return jsonify({
          'success': True,
          'questions': questions_formatted,
          'total_questions': len(questions),
          'current_category': None,
        })

      else:
        abort(404)

    except Exception as e:
      if '404' in str(e):
        abort(404)
      else:
        abort(422)

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    ''' Retrieve questions based on category. '''

    try:
      # Get page
      page = request.args.get('page', 1, type=int)

      # Query questions with category_id and paginate
      questions = Question.query.order_by(Question.id) \
        .filter(Question.category == category_id) \
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

  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    ''' Get questions to play the quiz. '''

    # try:
      # Retrieve raw data
    data = request.get_json()

    if not ('quiz_category' in data and 'previous_questions' in data):
      abort(422)
    
    quiz_category = data.get('quiz_category')
    previous_questions = data.get('previous_questions')
    category_id = quiz_category.get('id')

    if category_id == '0':
      # If no category specified, get all questions
      questions = Question.query.filter(
        Question.id.notin_((previous_questions))).all()
    else:
      # Else get questions by requested category
      questions = Question.query \
        .filter(Question.category == category_id) \
        .filter(Question.id.notin_((previous_questions))) \
        .all()

    new_question = questions[random.randrange(
      0, len(questions))].format() if len(questions) > 0 else None

    return jsonify({
      'success': True
    })

    # except Exception:
    #   abort(422)

  @app.errorhandler(400)
  def bad_request(error):
    print(error)
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    print(error)
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    print(error)
    return jsonify({
      'success': False, 
      'error': 422,
      'message': 'Unprocessable'
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    print(error)
    return jsonify({
      'success': False, 
      'error': 500,
      'message': 'Internal server error'
    }), 500

  return app
    