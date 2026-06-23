from django.contrib import admin
from .models import Question, Option, Result, UserResponse

class OptionInline(admin.TabularInline):
    """Варианты ответа отображаются прямо на странице вопроса"""
    model = Option
    extra = 1
    fields = ('text', 'score', 'order')
    ordering = ('order',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'order', 'question_type', 'category', 'is_active')
    list_filter = ('question_type', 'is_active', 'category')
    search_fields = ('text',)
    ordering = ('order',)
    inlines = [OptionInline]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'min_score', 'max_score', 'order')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    ordering = ('category', 'order')

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'session_key', 'user', 'question', 'option', 'value', 'created_at')
    list_filter = ('question', 'created_at')
    search_fields = ('session_key', 'value')
    raw_id_fields = ('user', 'question', 'option')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)