from django.contrib import admin
from .models import Board, TaskList, Card

admin.site.register(Board)
admin.site.register(TaskList)
admin.site.register(Card)