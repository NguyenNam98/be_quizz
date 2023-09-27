from collections import OrderedDict
from .models import Question, Answer, Quizz, User_response
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
    quizz_id = serializers.UUIDField()
    answer = serializers.ListField()


class UserResponseSerializer(serializers.Serializer):
    quizz = QuizzSerializer(many=True, read_only=True)

    class Meta:
            model = User_response
            fields = '__all__'

    def create(self, validated_data):
        # Create and return a new User_response instance based on the validated data
        return User_response.objects.create(**validated_data)