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