import json
from json import JSONDecodeError
from django.http import JsonResponse
from .serializers import QuizzSerializer, QuestionSerializer, AnswerSerializer, AnswerCheckSerializer
from .models import Quizz, Question, Answer
from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from django.shortcuts import get_object_or_404  # Import the get_object_or_404 function



class QuizViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    A simple ViewSet for listing or retrieving items.
    """
    # permission_classes = (IsAuthenticated,)
    queryset = Quizz.objects.all()
    serializer_class = QuizzSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        # Include related questions and answers in the response
        questions = Question.objects.filter(quizz_id=data['id'])
        question_serializer = QuestionSerializer(questions, many=True).data
        data['questions'] = question_serializer
        for question_data in data['questions']:
            question_id = question_data['id']
            answers = Answer.objects.filter(question_id=question_id)
            answer_serializer = AnswerSerializer(answers, many=True).data
            question_data['answers'] = answer_serializer
        return Response(data)

class AnswerCheckAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        serializer = AnswerCheckSerializer(data=data)
        if serializer.is_valid():
            question_id = serializer.validated_data['question_id']
            selected_answers = serializer.validated_data['selected_answers']

            # Use get_object_or_404 to retrieve the question or return a 404 response
            question = get_object_or_404(Question, pk=question_id)
            # Get the correct answers for the question from the Answer model
            correct_answers = Answer.objects.filter(question_id=question, is_correct=True)

            # Get the IDs of the correct answers
            correct_answer_ids = set(correct_answers.values_list('id', flat=True))

            # Check if selected_answers contain all correct answer IDs
            is_correct = set(selected_answers) == correct_answer_ids

            return Response({'is_correct': is_correct})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)