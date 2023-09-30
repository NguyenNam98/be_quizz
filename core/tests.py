import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Quizz, Question, Answer

class QuizViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.quizz = Quizz.objects.create(title="Test Quiz")
        self.question = Question.objects.create(quizz_id=self.quizz, question_text="Test Question")
        self.answer1 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 1", is_correct=True)
        self.answer2 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 2", is_correct=False)
        self.answer3 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 3", is_correct=False)
        self.answer4 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 4", is_correct=False)

    def test_list_quizzes_success(self):
        response = self.client.get('/api/quizz')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('completed', response.data)
        self.assertIn('new', response.data)
        self.assertEqual(len(response.data['new']), 1)
        self.assertEqual(len(response.data['completed']), 0)

    def test_retrieve_quiz_success(self):
        response = self.client.get(f'/api/quizz/{self.quizz.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.quizz.id))
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 1)

    def test_retrieve_quiz_not_found(self):
        id_test = '3414d7e0-0905-4836-8f6e-fcbbdef97ce3'
        response = self.client.get(f'/api/quizz/{id_test}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_quiz_params_not_uuid(self):
        id_test = '3414d7e0-0905-4836-8f6e-fcbbdef97ce33'
        response = self.client.get(f'/api/quizz/{id_test}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AnswerCheckAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.quizz = Quizz.objects.create(title="Test Quiz")
        self.question = Question.objects.create(quizz_id=self.quizz, question_text="Test Question")
        self.answer1 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 1", is_correct=True)
        self.answer2 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 2", is_correct=False)
        self.answer3 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 3", is_correct=False)
        self.answer4 = Answer.objects.create(question_id=self.question, answer_text="Test Answer 4", is_correct=False)

        self.question2 = Question.objects.create(quizz_id=self.quizz, question_text="Test Question")
        self.answer12 = Answer.objects.create(question_id=self.question2, answer_text="Test Answer 1", is_correct=True)
        self.answer22 = Answer.objects.create(question_id=self.question2, answer_text="Test Answer 2", is_correct=False)
        self.answer32 = Answer.objects.create(question_id=self.question2, answer_text="Test Answer 3", is_correct=False)
        self.answer42 = Answer.objects.create(question_id=self.question2, answer_text="Test Answer 4", is_correct=False)


    def test_check_answers_success(self):
        data = {
            'quizz_id': self.quizz.id,
            'answer': [
                {
                    'question_id': self.question.id,
                    'selected_answer': [self.answer1.id]
                },
                {
                    'question_id': self.question2.id,
                    'selected_answer': [self.answer22.id]
                }
            ]
        }
        response = self.client.post('/api/check-answer', data, format='vnd.api+json')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('score', response.data)
        self.assertEqual(response.data['score'], '1/2')

    def test_check_answers_fail_body_request(self):
        data = {
            # 'quizz_id': self.quizz.id,
            'answer': [
                {
                    'question_id': self.question.id,
                    'selected_answer': [self.answer1.id]
                },
                {
                    'question_id': self.question2.id,
                    'selected_answer': [self.answer22.id]
                }
            ]
        }
        response = self.client.post('/api/check-answer', data, format='vnd.api+json')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

