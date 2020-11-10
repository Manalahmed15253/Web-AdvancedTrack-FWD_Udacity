import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('', self.database_name)
        setup_db(self.app, self.database_path)
        self.new_question = {
            "question" : "What is the color of the sky",
            "answer" : "blue",
            "category" : 2,
            "difficulty" : 1
        }

        # binds the app to the current context
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
    def test_get_paginate_questions(self):
        """Test the get questions API for successing"""
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))


    def test_404_sent_requesting_beyond_valied_page(self):
        """Test the get questions API error"""
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found')

    def test_delete_question(self):
        """Test the delete question API for successing"""
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question,None)
    
    def test_422_if_question_does_not_exist(self):
        """Test the delete question API error"""
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')

    def test_post_new_question(self):
        """Test the post question API for successing"""
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)


        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_405_if_question_creation_not_allowed(self):
        """Test the delete question API error"""
        res = self.client().post('/questions/45',json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'method not allowed')
    
    def test_post_get_searched_question(self):
        """Test the post endpoint to get questions based on a search term API for successing"""
        res = self.client().post('/questions/search', json={'searchTerm': "is"})
        data = json.loads(res.data)


        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_400_if_question_search_not_correctly_formatted(self):
        """Test the post endpoint to get questions based on a search term API for error"""
        res = self.client().post('/questions/search')
        data = json.loads(res.data)


        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'bad request')
    
    def test_get_questions_by_category(self):
        """Test the get endpoint to get questions based on a given category id for successing"""
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'],1)
    
    def test_422_if_category_does_not_exist(self):
        """Test the get endpoint to get questions based on a given category id for error"""
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'unprocessable')
    
    def test_play_quiz(self):
        """Test the post endpoint to play for successing"""
        res = self.client().post('/quizzes',json={'quiz_category': {'type':'Science','id' : '1'},'previous_questions' : [21]})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'],1)
        self.assertNotEqual(data['question']['id'],21)
    
    def test_failed_quiz(self):
        """Test the post endpoint to play for error"""
        res = self.client().post('/quizzes',json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code,400)
        self.assertEqual(data['success',False])
        self.assertEqual(data['message','bad request']) 

        



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()