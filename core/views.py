import json
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    QuizzSerializer,
    QuestionSerializer,
    AnswerSerializer,
    AnswerCheckSerializer,
    UserResponseSerializer,
    QuizzResultSerializer
)
from .models import Quizz, Question, Answer, User_response, User_quizz_result
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404  # Import the get_object_or_404 function
from django.contrib.auth.models import User


class QuizViewSet(
    viewsets.ModelViewSet
):
    """
    A simple ViewSet for listing or retrieving items.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer
    lookup_field = 'id'

    def list(self, request, *args, **kwargs):
        user_name = request.user
        user_query = User.objects.filter(username=user_name)
        user_id = user_query.first().id

        completed_quizzes = User_quizz_result.objects.filter(user_id=user_id).values()
        completed = []
        for completed_quizz in completed_quizzes:
            response_quizz_completed = {}
            response_quizz_completed['result_id'] = str(completed_quizz['id'])
            quizz_id = completed_quizz['quizz_id_id']
            response_quizz_completed['quizz_info'] = Quizz.objects.filter(id=quizz_id).values().first()
            response_quizz_completed['score'] = completed_quizz['score']
            completed.append(response_quizz_completed)
        new_quizzes = Quizz.objects.exclude(id__in=completed_quizzes.values_list('quizz_id', flat=True))

        data = {}
        data['completed'] = completed
        data['new'] = self.get_serializer(new_quizzes, many=True).data

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        quizz_id = kwargs['id']
        try:
            instance = get_object_or_404(Quizz, id=quizz_id)
        except:
            return Response('Check params', status=status.HTTP_404_NOT_FOUND)

        data = self.get_serializer(instance).data

        questions = Question.objects.filter(quizz_id=data['id'])
        question_serializer = QuestionSerializer(questions, many=True).data
        data['questions'] = question_serializer

        for question_data in data['questions']:
            question_id = question_data['id']
            answers = Answer.objects.filter(question_id=question_id)
            answer_serializer = AnswerSerializer(answers, many=True).data
            question_data['answers'] = answer_serializer

        return Response(data, status=status.HTTP_200_OK)


class AnswerCheckAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        user_name = request.user
        user_query = User.objects.filter(username=user_name)
        user_id = user_query.first()

        serializer = AnswerCheckSerializer(data=data)

        if serializer.is_valid():
            quizz_id = serializer.validated_data['quizz_id']
            answer = serializer.validated_data['answer']
            # Use get_object_or_404 to retrieve the question or return a 404 response
            quizz = get_object_or_404(Quizz, id=quizz_id)
            result = []
            user_database = []
            right_answer_count = 0
            for answer_data in answer:
                question_id = answer_data['question_id']
                selected_answer_ids = answer_data['selected_answer']
                question = get_object_or_404(Question, id=question_id)

                correct_answers = Answer.objects.filter(question_id=question_id, is_correct=True)
                selected_answers = Answer.objects.filter(id__in=selected_answer_ids)
                is_correct = set(selected_answers) == set(correct_answers)

                result.append({"question_id": question_id, "is_correct": is_correct})
                if is_correct:
                    right_answer_count += 1
                user_response_data = {
                    'user_id': user_id,
                    'quizz_id': quizz,
                    'question_id': question,
                    'selected_answer_ids': json.dumps([str(item) for item in selected_answer_ids]),
                }

                user_response_serializer = UserResponseSerializer(data=user_response_data)

                if user_response_serializer.is_valid():
                    # UserResponseSerializer.create(self, user_response_data)
                    user_database.append(user_response_data)

            score = f'{right_answer_count}/{len(answer)}'
            data_user_quizz_result = {
                'score': score,
                'user_id': user_id,
                'quizz_id': quizz,
            }
            quizz_result_check = QuizzResultSerializer(data=data_user_quizz_result)
            if quizz_result_check.is_valid():
                result_create = QuizzResultSerializer.create(self, data_user_quizz_result)
                for item in user_database:
                    item['result_id'] = result_create
                    UserResponseSerializer.create(self, item)
                return Response({'score': score}, status=status.HTTP_200_OK)

        return Response('Body request wrong', status=status.HTTP_400_BAD_REQUEST)


class QuizzReviewView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        result_id = kwargs['id']
        result_user_response = User_quizz_result.objects.filter(id=result_id)
        time_completed = result_user_response.values().first()['created']
        if result_user_response.exists():
            quizz_id = result_user_response.first().quizz_id
            quizz_id_str = result_user_response.values().first()['quizz_id_id']
            quizz_info = Quizz.objects.filter(id=quizz_id_str).values()
            if quizz_info.exists() is False:
                Response('No results', status=status.HTTP_404_NOT_FOUND)
            score = result_user_response.first().score
            user_answer = User_response.objects.filter(result_id=result_id).values()
            user_answer_objects = {item['question_id_id']: item for item in list(user_answer)}
            questions_of_quizz = Question.objects.filter(quizz_id=quizz_id).values()
            answers_right_of_questions = []
            for question in questions_of_quizz:
                answer_right = Answer.objects.filter(question_id=question['id'], is_correct=True).values()
                all_answer = Answer.objects.filter(question_id=question['id']).values()
                answer_right_ids = [item['id'] for item in answer_right]
                question['answers'] = all_answer
                answers_right_of_questions.append({
                    'question': question,
                    'correct_answer': answer_right_ids,
                    'user_response_answer': json.loads(user_answer_objects[question['id']]['selected_answer_ids']),
                })

            return Response({
                'answer': answers_right_of_questions,
                'score': score,
                'quizz_info': quizz_info,
                'time_completed': time_completed,
            },
                status=status.HTTP_200_OK)
        return Response('No results', status=status.HTTP_404_NOT_FOUND)


