import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages

from .models import (
    Choice,
    Question,
    Task
)
from .process import (
    A010_Index,
    A020_GoToRegistTask,
    A030_RegistTask,
    A040_GoToDetailTask,
    A050_UpdateTask,
    A060_DeleteTask,
    S006_GetKeibaNews
)
from .process import C010_Const

#DS 2021/10/03 クラス構成対応
#共通処理
#一覧用のコンテキストを作成する
#def make_context_index():
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    #AS 20210927
#    all_task_list = Task.objects.filter(delflg="0").order_by('id')
#    #AE 20210927
#    context = {'latest_question_list': latest_question_list,
#                'all_task_list': all_task_list,
#                }
#    return context
#DE 2021/10/03 クラス構成対応

#共通メソッド-----------------------------------------------------------------------------------------------------
def setMessages(request,list_msg):
    """
    C:\Python39\Lib\site-packages\django\contrib\messages
    messages.constants.ERROR...
    ⇒C010_Const.pyにて再定義したため、こちらを利用
        DEBUG = 10
        INFO = 20
        SUCCESS = 25
        WARNING = 30
        ERROR = 40
    使用例）
    (1)下記のように、"level"と"msg"で1つのjsonを作成する。この際、「C010_Const」からエラーレベルを選択する。
        json_msg={"level":C010_Const.ERROR,"msg":"タイトルが未入力です"}
    (2)下記のように、list_msgに作成したメッセージ情報を追加する、
        list_msg.append(json_msg)
    """
    for json_msg in list_msg:
        #messages.error(request, massage)
        messages.add_message(request,json_msg["level"], json_msg["msg"])
#-----------------------------------------------------------------------------------------------------------------


#目次
def index(request):
    #CS 2021/10/03 クラス構成対応
    #context = make_context_index()
    #print(type(request))
    #print(request)
    #print(type(request.POST))
    #print(request.POST)
    #print(type(request.GET))
    #print(request.GET)
    list_msg = []
    json_main = A010_Index.main(request,list_msg)
    context = json_main["context"]
    template = json_main["template"]
    #CE 2021/10/03 クラス構成対応
    setMessages(request,list_msg)
    return render(request, template, context)

#タスク登録画面に遷移
def goto_regist_task(request):
    list_msg = []
    json_main = A020_GoToRegistTask.main(request,list_msg)
    context = json_main["context"]
    template = json_main["template"]
    setMessages(request,list_msg)
    return render(request, template, context)

#タスク詳細画面に遷移
def goto_detail_task(request,task_id):
    list_msg = []
    json_main = A040_GoToDetailTask.main(request,list_msg,task_id)
    context = json_main["context"]
    template = json_main["template"]
    setMessages(request,list_msg)
    return render(request, template, context)

#タスク更新
def update_task(request):
    list_msg = []
    json_main = A050_UpdateTask.main(request,list_msg)
    context = json_main["context"]
    template = json_main["template"]
    setMessages(request,list_msg)
    return render(request, template, context)

#タスク登録
def regist_task(request):
    #メッセージリストを宣言
    list_msg = []
    #アクションクラスを呼び出し
    json_main = A030_RegistTask.main(request,list_msg)
    #引数用のコンテキスト、遷移先を取得
    context = json_main["context"]
    template = json_main["template"]
    #メッセージをセット
    setMessages(request,list_msg)
    #返却
    return render(request, template, context)
    """
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'TaskManagement/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return render(request, 'TaskManagement/regist_task.html')
    """

    #タスク削除（論理削除）
def delete_task(request):
    #メッセージリストを宣言
    list_msg = []
    #アクションクラスを呼び出し
    json_main = A060_DeleteTask.main(request,list_msg)
    #引数用のコンテキスト、遷移先を取得
    context = json_main["context"]
    template = json_main["template"]
    #メッセージをセット
    setMessages(request,list_msg)
    #返却
    return render(request, template, context)


    #テスト01
def test01(request):
    #list_newsInfo = S006_GetKeibaNews.main(0)
    #メッセージリストを宣言
    template = "TaskManagement/test01.html"
    #context = {"list_newsInfo":list_newsInfo}
    context = {}
    #返却
    return render(request, template, context) 

#===============================================================================================================
#オルフェーブル
def olfe(request, question_id):
    return HttpResponse("You're オルフェーブル No %s." % question_id)

#文字フェーブル
def str_olfe(request, question_text):
    return HttpResponse("You're %sフェーブル" % question_text)

#詳細
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'TaskManagement/detail.html', {'question': question})

#結果
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'TaskManagement/results.html', {'question': question})

#投票
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'TaskManagement/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('TaskManagement:results', args=(question.id,)))