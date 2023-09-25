from collections import OrderedDict
from .models import Question, Answer, Quizz
from rest_framework_json_api import serializers
from rest_framework import status
from rest_framework.exceptions import APIException




class questionNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This question not found'
    default_code = 'invalid'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'id',
            'answer_text'
        ]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = '__all__'


class QuizzSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quizz
        fields = '__all__'


class AnswerCheckSerializer(serializers.Serializer):
    question_id = serializers.UUIDField()
    selected_answers = serializers.ListField(child=serializers.UUIDField())