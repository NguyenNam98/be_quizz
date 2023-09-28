import json
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    QuizzSerializer,
    QuestionSerializer,
    AnswerSerializer,
    AnswerCheckSerializer,
    UserResponseSerializer
)
from .models import Quizz, Question, Answer, User_response
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

        completed_quizzes = User_response.objects.filter(user_id=user_id)
        completed = Quizz.objects.filter(id__in=completed_quizzes.values_list('quizz_id', flat=True))
        new_quizzes = Quizz.objects.exclude(id__in=completed_quizzes.values_list('quizz_id', flat=True))

        data = {}
        data['completed'] = QuizzSerializer(completed, many=True).data
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

            for answer_data in answer:
                question_id = answer_data['question_id']
                selected_answer_ids = answer_data['selected_answer']
                question = get_object_or_404(Question, id=question_id)

                correct_answers = Answer.objects.filter(question_id=question_id, is_correct=True)
                selected_answers = Answer.objects.filter(id__in=selected_answer_ids)
                is_correct = set(selected_answers) == set(correct_answers)

                result.append({"question_id": question_id, "is_correct": is_correct})
                user_response_data = {
                    'user_id': user_id,
                    'quizz_id': quizz,
                    'question_id': question,
                    'selected_answer_ids': f'{selected_answer_ids}'
                }

                user_response_serializer = UserResponseSerializer(data=user_response_data)

                if user_response_serializer.is_valid():
                    UserResponseSerializer.create(self, user_response_data)
                else:
                    return Response(user_response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'result': result}, status=status.HTTP_200_OK)

        return Response('Body request wrong', status=status.HTTP_400_BAD_REQUEST)
