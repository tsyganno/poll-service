from django.urls import path
from app_poll.views import IndexView, VoteView, QuestionView, VariantView, TextAnswerView, record_to_model_one_answer, \
    SomeVariantView, record_to_model_some_answers, OutcomeView, QuestionByTypeView, DeleteAnswerView


app_name = 'poll'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('votes/', VoteView.as_view(), name='vote'),
    path('votes/<int:pk>/', QuestionView.as_view(), name='question'),
    path('votes/question/<int:pk>/<str:type>/', QuestionByTypeView.as_view(), name='question_by_type'),
    path('votes/one_answer_question/<int:pk>/', VariantView.as_view(), name='variant'),
    path('votes/one_answer_question/result/<int:pk>/', record_to_model_one_answer, name='result_one_variant'),
    path('votes/some_answers_question/<int:pk>/', SomeVariantView.as_view(), name='some_variant'),
    path('votes/some_answers_question/result/<int:pk>/', record_to_model_some_answers, name='result_some_variant'),
    path('votes/text_one_answer_question/<int:pk>/', TextAnswerView.as_view(), name='text_answer'),
    path('outcome/<int:pk>/', OutcomeView.as_view(), name='outcome'),
    path('delete/<int:pk>/', DeleteAnswerView.as_view(), name='delete'),
]
