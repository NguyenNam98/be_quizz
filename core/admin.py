from django.contrib import admin
from . import models


@admin.register(models.Quizz)
class Quizz(admin.ModelAdmin):
    list_display = ('id', 'title', 'description')


@admin.register(models.Question)
class Question(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'is_single_choice')


@admin.register(models.Answer)
class Answer(admin.ModelAdmin):
    list_display = ('id', 'answer_text', 'is_correct')


@admin.register(models.User_response)
class UserResponse(admin.ModelAdmin):
    list_display = ('id', 'quizz_id', 'question_id', 'selected_answer_ids', 'user_id')