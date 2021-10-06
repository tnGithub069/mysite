from django.urls import path

from . import views
#AS 20210929 画像対応
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#AE 20210929 画像対応

app_name = 'TaskManagement'
urlpatterns = [
    #Index.html
    path('', views.index, name='index'),
    #AS 20210926
    # ex: /TaskManagement/5/
    #path('<int:question_id>/', views.detail, name='detail'),
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    # ex: /TaskManagement/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /TaskManagement/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # ex: /TaskManagement/5/olfe/
    path('<int:question_id>/olfe/', views.olfe, name='olfe'),
    # ex: /TaskManagement/5/olfe/
    path('<str:question_text>/str_olfe/', views.str_olfe, name='str_olfe'),
    #AE 20210926
    #AS 20210928
    path('regist_task/', views.goto_regist_task, name='goto_regist_task'),
    path('registed_task/', views.regist_task, name='regist_task'),
    path('detail_task/<int:task_id>/', views.goto_detail_task, name='detail_task'),
    path('update_task/', views.update_task, name='update_task'),
    path('delete_task/', views.delete_task, name='delete_task'),
    #AE 20210928
] + static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)
