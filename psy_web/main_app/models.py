from django.db import models
from django.conf import settings


class Question(models.Model):
    TYPE_CHOICES = (
        ('single', 'Одиночный выбор'),
        ('multiple', 'Множественный выбор'),
        ('scale', 'Шкала (числовое значение)'),
        ('text', 'Текстовый ввод'),   # новый тип
    )
    text = models.TextField(verbose_name='Текст вопроса')
    order = models.PositiveIntegerField(verbose_name='Порядковый номер', default=0)
    category = models.CharField(max_length=50, blank=True, verbose_name='Категория')
    question_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='single')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255, verbose_name='Текст ответа')
    score = models.IntegerField(default=0, verbose_name='Балл')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text[:30]


class Result(models.Model):
    category = models.CharField(max_length=50, blank=True, verbose_name='Категория')
    title = models.CharField(max_length=100, verbose_name='Название результата')
    description = models.TextField(verbose_name='Описание')
    min_score = models.IntegerField(verbose_name='Минимальный балл')
    max_score = models.IntegerField(verbose_name='Максимальный балл')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f"{self.title} ({self.min_score}–{self.max_score})"


class UserResponse(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Пользователь'
    )
    session_key = models.CharField(max_length=40, blank=True, db_index=True, verbose_name='Ключ сессии')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=255, blank=True, verbose_name='Введённое значение')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Уникальность: один пользователь/сессия – один ответ на вопрос
        unique_together = [['user', 'question'], ['session_key', 'question']]

    def __str__(self):
        return f"{self.user or self.session_key} – {self.question.text[:20]}"