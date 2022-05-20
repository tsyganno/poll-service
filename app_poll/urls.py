from django.urls import path
from app_poll.views import IndexView, VoteView, QuestionView, VariantView, TextAnswerView, proba


app_name = 'poll'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('votes/', VoteView.as_view(), name='vote'),
    path('votes/<int:pk>/', QuestionView.as_view(), name='question'),
    path('votes/one_answer_question/<int:pk>/', VariantView.as_view(), name='variant'),
    path('votes/one_answer_question/result/<int:pk>/', proba, name='result_one_variant'),
    path('votes/text_one_answer_question/<int:pk>/', TextAnswerView.as_view(), name='text_answer'),
]
