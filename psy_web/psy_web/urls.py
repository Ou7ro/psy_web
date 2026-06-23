from django.urls import path
from main_app import views
from django.contrib import admin

urlpatterns = [
    path('', views.test_view, name='test'),
    path('result/', views.result_view, name='result'),
    path('admin/', admin.site.urls),
]
