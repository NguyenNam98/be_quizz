from django.db import models
from django.contrib.auth.models import User
from utils.model_abstracts import Model
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)


class Quizz(
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel,
    Model
):
    class Meta:
        verbose_name = 'Quizz'
        verbose_name_plural = 'Quizzes'
        ordering = ["id"]


class Question(
    TimeStampedModel,
    Model
):
    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        ordering = ["id"]

    # item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500, blank=False, null=False, default='')
    is_single_choice = models.BooleanField(default=True)
    quizz_id = models.ForeignKey(Quizz, on_delete=models.CASCADE)


class Answer(
    TimeStampedModel,
    Model
):
    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ["id"]

    answer_text = models.CharField(max_length=500, blank=False, null=False, default='')
    is_correct = models.BooleanField(default=False)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

class User_responses(
    TimeStampedModel,
    Model
):
    class Meta:
        verbose_name = 'User_response'
        verbose_name_plural = 'User_responses'
        ordering = ["id"]

    selected_answer_ids = models.TextField(default='[]')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    quizz_id = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

