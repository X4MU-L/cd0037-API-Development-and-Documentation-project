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
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','callONme','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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




    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))


    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertIsInstance(data["total_questions"], int)
        self.assertTrue(len(data["categories"]))
        self.assertFalse(data["current_category"])


    def test_get_paginated_questions_bad_req(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resorses not found")


    def test_delete_questions(self):
        res = self.client().delete("/questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted_id"], 1)
        self.assertTrue(data["total_questions"])
        self.assertIsInstance(data["total_questions"], int)
        

    def test_delete_not_found(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resorses not found")


    def test_create_question(self):
        question = {
            "question":"what year are we in?",
            "answer": 2022,
            "difficulty":1,
            "category":2,
        }
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["created_question"], question["question"])
        self.assertTrue(data["created_id"])
        self.assertTrue(len(data["questions"]))
        self.assertIsInstance(data["created_id"], int)
        self.assertIsInstance(data["total_questions"], int)

    def test_search_questions(self):
        search ={
            "searchTerm": "In which"
        }
        res = self.client().post('/questions', json=search)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["total_questions"], 2)
        self.assertFalse(data["current_category"])


    def test_create_question_bad_data(self):
        question = {
            "question":"what year are we in?",
            "answer": 2022,
            "difficulty":"hard",
            "category":"Arts",
        }
        res = self.client().post('/questions', json=question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    def test_create_question_no_body(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")


    def test_search_questions_not_found(self):
        search ={
            "searchTerm": "In which country"
        }
        res = self.client().post('/questions', json=search)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertFalse(len(data["questions"]))
        self.assertEqual(data["total_questions"], 0)
        self.assertFalse(data["current_category"])
        

    def test_get_trivia_quizzes(self):
        quiz ={
            "previous_questions": [],
            "quiz_category":{
                "id":"1", 
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
    

    def test_get_trivia_quizzes_force_end(self):
        quiz ={
            "previous_questions": [],
            "quiz_category":{
                "id":"1000", 
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertFalse(data["question"])


    def test_get_trivia_quizzes_bad_request(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")


    def test_get_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        print(data)

        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["current_category"])
        self.assertIsInstance(data["total_questions"], int)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()