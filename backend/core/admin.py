from django.contrib import admin
from . import models


@admin.register(models.Quizz)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(models.Question)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text', 'is_single_choice')


@admin.register(models.Answer)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_text', 'is_correct')


@admin.register(models.User_response)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'quizz_id', 'question_id', 'selected_answer_ids')