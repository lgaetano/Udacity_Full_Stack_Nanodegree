import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from __init__ import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    '''This class represents the trivia test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = 'postgresql://postgres:1234@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        self.new_question = { 
            'id': 24,
            'question': 'TEST TEST TEST',
            'answer': 'TEST ANSWER',
            'difficulty': 2,
            'category': 1
        }

        self.new_quiz = {
            'previous_questions': [],
            'quiz_category': {
                'type': 'Sports',
                'id': 11
            }
        }

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        '''Executed after reach test.'''
        pass

    def test_get_questions(self):
        '''Test question retrieval.'''

        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))
    
    def test_404_question_outside_paginated_range(self):
        '''Test for question outside paginated range.'''

        res = self.client().get('/questions?page=75')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_quesion(self):
        '''Test creating a question.''' 

        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_get_category(self):
        '''Test category retrieval.'''

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)

    def test_404_question_outside_paginated_range(self):
        '''Test for question outside paginated range.'''

        res = self.client().get('/questions?page=75')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_get_questions_by_category(self):
        '''Test retrieval of questions by category'''

        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        self.assertTrue(len(data['questions']))

    def test_404_question_by_category_outside_paginated_range(self):
        '''Test for question by category outside paginated range.'''

        res = self.client().get('/categories/1/questions?page=75')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    def test_delete_question(self):
        '''Test question deletion.'''
        
        # question = self.new_question
        question = Question(
            question= 'DELETE TEST',
            answer= 'DELETE TEST ANSWER',
            difficulty= 2,
            category= 1)
        question.insert()
        quesiton_id = question.id
        # quesiton_id = 24

        res = self.client().delete('/questions/{question_id}')
        data = json.loads(res.data)

        question = Question.query.filter(
            Question.id == question.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], str(question_id))
        self.assertEqual(question, None)

    def test_422_delete_question_does_not_exist(self):
        '''Test deletion of a question that doesn't exist.'''

        res = self.client().delete('/questions/75')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_search_questions(self):
        '''Test search endpoint.'''

        res = self.client().post('/questions/search', json={'searchTerm': 'a'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertIsNotNone(data['total_questions'])

    def test_404_search_question_no_result(self):
        '''Search for a question where there is no result'''

        res = self.client().post('/questions/search', json={'searchTerm': 'blamo'})
        data = json.load(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], True)

        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(data['current_category'], None)
    
    def test_quizzes(self):
        '''Test quiz game play endpoint.'''

        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()