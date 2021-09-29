from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    #Index.html
    path('', views.index, name='index'),
    #AS 20210926
    # ex: /polls/5/
    #path('<int:question_id>/', views.detail, name='detail'),
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /polls/5/olfe/
    path('<int:question_id>/olfe/', views.olfe, name='olfe'),
    # ex: /polls/5/olfe/
    path('<str:question_text>/str_olfe/', views.str_olfe, name='str_olfe'),
    #AE 20210926
]
