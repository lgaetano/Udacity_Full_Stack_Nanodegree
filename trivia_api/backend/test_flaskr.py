import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from __init__ import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = 'postgresql://postgres:1234@localhost:5432/trivia'
        setup_db(self.app, self.database_path)

        # Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        '''Testing question retrieval.'''

        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['sucess'], True)

        self.assertTrue(data['questions'])
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions'], 10))
        self.assertEqual(data['total_questions'], 19)

        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)
        self.assertEqual(data['current_category'], None)

    def test_get_questions(self):
        ''' Testing category retrieval'''

        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)
        self.assertIsInstance(data['categories'], dict)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()