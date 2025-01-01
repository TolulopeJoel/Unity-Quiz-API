from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register('', views.QuestionViewSet, basename='questions')

urlpatterns = [
    path('json/', views.QuestionListAPIView.as_view(), name='question-list-json'),
]

urlpatterns += router.urls
