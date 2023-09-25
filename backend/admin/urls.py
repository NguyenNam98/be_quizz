from django.urls import path, include
from django.contrib import admin
from rest_framework import routers
from core import views as quizz_view

router = routers.DefaultRouter()

urlpatterns = router.urls
router.register(r'quizz', quizz_view.QuizViewSet, basename='quizz')
# router.register(r'question', quizz_view.QuestionViewSet, basename='question')

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/quizz/<str:quizz_id>/', quizz_view.QuizViewSet.as_view({'get': 'list'}), name='quizz-list'),
    path('api/check-answer/', quizz_view.AnswerCheckAPIView.as_view(), name='check-answer'),
]
