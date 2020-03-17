#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json, os, unittest
from flask_sqlalchemy import SQLAlchemy
from .app import create_app
from .models import setup_db, Actor, Movie

#----------------------------------------------------------------------------#
# Tests
#----------------------------------------------------------------------------#

class AgencyTestCase(unittest.TestCase):
	"""This class represents the agency's test case"""

	def setUp(self):
		"""Define test variables and initialize app."""
		self.app = create_app()
		self.client = self.app.test_client
		self.database_name = "agency_test"
		self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
		setup_db(self.app, self.database_path)

		# binds the app to the current context
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			self.db.drop_all()
			# create all tables
			self.db.create_all()
	
	def tearDown(self):
		"""Executed after reach test"""
		pass

	def test_should_return_all_actors(self):
		# Insert dummy actor into database.
		actor = Actor(name="Leonardo Di Caprio", age="45", gender="male")
		actor.insert()

		res = self.client().get('/actors')
		print(res)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

		actors = Actor.query.all()
		self.assertEqual(len(data['actors']), len(actors))

	def test_get_actors_dont_accept_post_request(self):
		res = self.client().post('/actors')
		self.assertEqual(res.status_code, 405)

	# def test_should_get_first_page_questions(self):
	#     res = self.client().get('/questions')
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])
	#     # Makes sure the request is properly paginated.
	#     self.assertEqual(len(data['questions']), QUESTIONS_PER_PAGE)

	#     questions = Question.query.all()
	#     # Asserting that pagination worked.
	#     self.assertEqual(data['total_questions'], len(questions))

	# def test_should_allow_second_page_questions(self):
	#     res = self.client().get('/questions/2')
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])

	#     questions = Question.query.all()
	#     # Asserting that pagination worked.
	#     self.assertEqual(data['total_questions'], len(questions))

	#     # Makes sure the request is properly paginated.
	#     self.assertEqual(len(data['questions']), len(questions) - QUESTIONS_PER_PAGE)

	# def test_should_not_allow_third_page_questions(self):
	#     res = self.client().get('/questions/3')
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 404)
	#     self.assertEqual(data['error'], 404)
	#     self.assertFalse(data['success'])

	# def test_should_filter_questions_by_sports_category(self):
	#     res = self.client().get('/categories/6/questions')
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])

	#     sports_questions = Question.query.filter_by(category=6).all()
	#     self.assertEqual(data['total_questions'], len(sports_questions))

	# def test_should_not_return_second_page_of_sports_questions(self):
	#     res = self.client().get('/categories/6/questions/2')
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 404)
	#     self.assertEqual(data['error'], 404)
	#     self.assertFalse(data['success'])

	# def test_should_delete_question_by_id(self):
	#     question_id = 5
	#     res = self.client().delete('/questions/' + str(question_id))
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertEqual(data['success'], True)
	#     self.assertEqual(data['id'], question_id)

	# def test_should_return_not_found_when_question_id_doesnt_exist(self):
	#     res = self.client().delete('/questions/1')
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 404)
	#     self.assertTrue(data['error'], 404)
	#     self.assertFalse(data['success'])

	# def test_should_create_new_question(self):
	#     new_question_data = {
	#         'question': "Does the test create a new question?",
	#         'answer': "Question is created.",
	#         'category': 5,
	#         'difficulty': 5
	#     } 

	#     res = self.client().post('/questions', data=json.dumps(new_question_data), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])
	#     self.assertEqual(data['question']['question'], new_question_data['question'])
	#     self.assertEqual(data['question']['answer'], new_question_data['answer'])
	#     self.assertEqual(data['question']['category'], new_question_data['category'])
	#     self.assertEqual(data['question']['difficulty'], new_question_data['difficulty'])

	#     question_added = Question.query.get(data['question']['id'])
	#     self.assertTrue(question_added)

	# def test_should_not_allow_new_question_missing_answer(self):
	#     new_question_data = {
	#         'question': "Does the test create a new question?",
	#         'category': 5,
	#         'difficulty': 5
	#     } 

	#     res = self.client().post('/questions', data=json.dumps(new_question_data), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 400)
	#     self.assertEqual(data['error'], 400)
	#     self.assertFalse(data['success'])

	# def test_should_not_allow_new_question_with_invalid_difficulty(self):
	#     new_question_data = {
	#         'question': "Does the test create a new question?",
	#         'answer': "Question is created.",
	#         'category': 5,
	#         'difficulty': 10
	#     } 

	#     res = self.client().post('/questions', data=json.dumps(new_question_data), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 422)
	#     self.assertEqual(data['error'], 422)
	#     self.assertFalse(data['success'])

	# def test_should_return_valid_search_results(self):
	#     search_term = 'royal'
	#     search_json = {
	#         'searchTerm': search_term
	#     }

	#     res = self.client().post('/search', data=json.dumps(search_json), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])
		
	#     search_data = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
	#     question_ids = []
	#     for question in search_data:
	#         question_ids.append(question.id)
	#     self.assertEqual(len(search_data), data['totalQuestions'])
	#     for question in data['questions']:
	#         self.assertIn(question['id'], question_ids)

	# def test_should_have_no_search_results(self):
	#     search_term = 'Alaskdfhsoiewl'
	#     search_json = {
	#         'searchTerm': search_term
	#     }

	#     res = self.client().post('/search', data=json.dumps(search_json), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 404)
	#     self.assertEqual(data['error'], 404)
	#     self.assertFalse(data['success'])
		
	# def test_should_get_random_question_from_art(self):
	#     quiz_category = 4
	#     quizzes_request_data = {
	#         "category": quiz_category
	#     }
	#     res = self.client().post('/quizzes', data=json.dumps(quizzes_request_data), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])

	#     self.assertEqual(data['question']['category'], quiz_category)

	#     requested_question = Question.query.get(data['question']['id'])
	#     self.assertEqual(data['question']['category'], requested_question.category)

	# def test_should_not_return_previous_questions_passed(self):
	#     quiz_category = 4
	#     previous_questions_query = Question.query.filter_by(category=quiz_category).all()
	#     previous_questions = []

	#     for question in previous_questions_query:
	#         previous_questions.append(question.id)

	#     last_question = previous_questions.pop()

	#     quizzes_request_data = {
	#         "category": quiz_category,
	#         "previous_questions": previous_questions
	#     }

	#     res = self.client().post('/quizzes', data=json.dumps(quizzes_request_data), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 200)
	#     self.assertTrue(data['success'])

	#     requested_question = Question.query.get(data['question']['id'])
	#     self.assertEqual(data['question']['id'], last_question)

	# def test_should_not_return_any_more_questions(self):
	#     quiz_category = 4
	#     previous_questions_query = Question.query.filter_by(category=quiz_category).all()
	#     previous_questions = []

	#     for question in previous_questions_query:
	#         previous_questions.append(question.id)

	#     quizzes_request_data = {
	#         "category": quiz_category,
	#         "previous_questions": previous_questions
	#     }

	#     res = self.client().post('/quizzes', data=json.dumps(quizzes_request_data), headers={'Content-Type': 'application/json'})
	#     data = json.loads(res.data)

	#     self.assertEqual(res.status_code, 404)
	#     self.assertTrue(data['error'], 404)
	#     self.assertFalse(data['success'])

# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()