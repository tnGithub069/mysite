import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question, Task

#共通処理
#一覧用のコンテキストを作成する
def make_context_index():
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #AS 20210927
    all_task_list = Task.objects.filter(delflg="0").order_by('id')
    #AE 20210927
    context = {'latest_question_list': latest_question_list,
                'all_task_list': all_task_list,
                }
    return context

#目次
def index(request):
    context = make_context_index()
    return render(request, 'TaskManagement/index.html', context)

#タスク登録画面に遷移
def goto_regist_task(request):
    today = datetime.datetime.now()
    today = format(today, '%Y-%m-%d')
    context = {'today':today}
    return render(request, 'TaskManagement/regist_task.html',context)

#タスク詳細画面に遷移
def goto_detail_task(request,task_id):
    #task_deail = get_object_or_404(Task, pk='4')
    list_one_task = Task.objects.all().filter(id=task_id)
    print("QuerySet型確認",type(list_one_task))
    hyoji_kigen = list_one_task[0].task_kign
    print("Datetime型確認",type(hyoji_kigen))
    hyoji_kigen = format(hyoji_kigen, '%Y-%m-%d')
    print(hyoji_kigen)

    context = {'list_one_task': list_one_task,
                'hyoji_kigen': hyoji_kigen,
                }
    return render(request, 'TaskManagement/detail_task.html',context)

#タスク更新
def update_task(request):
    #task_deail = get_object_or_404(Task, pk='4')
    #(1)画面パラメータから値を取得する
    task_id = request.POST['task_id']
    task_title = request.POST['task_title']
    task_tant = request.POST['task_tant']
    task_kign = request.POST['task_kign']
    task_kihyb = datetime.datetime.now()
    task_detail = request.POST['task_detail']
    task_log = request.POST['task_log']
    task_status = request.POST['task_status']
    #(2)テーブルを更新する
    #Store.objects.values().filter(name__istartswith='st').update(registered_users=F('registered_users') + 1)
    Task.objects.values().filter(id=task_id).update(
        task_title = task_title,
        task_tant = task_tant,
        task_kign = task_kign,
        task_kihyb = task_kihyb,
        task_detail = task_detail,
        task_log = task_log,
        task_status = task_status,
        )
    #(3)更新後の値を取得する
    list_one_task = Task.objects.all().filter(id=task_id)
    #(4)表示期限を取得
    hyoji_kigen = list_one_task[0].task_kign
    hyoji_kigen = format(hyoji_kigen, '%Y-%m-%d')
    #(5)コンテキストを作成
    context = {'list_one_task': list_one_task,
                'hyoji_kigen': hyoji_kigen,
                }
    return render(request, 'TaskManagement/detail_task.html',context)

#タスク登録
def regist_task(request):
    #(1)画面からデータを取得する
    #question = get_object_or_404(Question, pk=question_id)
    task_title = request.POST['task_title']
    task_tant = request.POST['task_tant']
    task_kign = request.POST['task_kign']
    task_kihyb = datetime.datetime.now()
    task_detail = request.POST['task_detail']
    task_log = request.POST['task_log']
    task_status = request.POST['task_status']
    print(task_title)
    print(task_tant)
    print(task_kign)
    print(task_detail)
    print(task_log)
    #(2)テーブルにレコードを作成する
    Task.objects.create(task_title=task_title,
                        task_tant=task_tant,
                        task_kihyb = task_kihyb,
                        task_kign=task_kign,
                        task_detail=task_detail,
                        task_log=task_log,
                        task_status=task_status,
                        delflg="0",
                        )
    #一覧用コンテキストを作成
    context = make_context_index()
    return render(request, 'TaskManagement/index.html',context)
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
    #task_deail = get_object_or_404(Task, pk='4')
    #(1)画面パラメータから削除所対象のPkeyを取得する
    task_id = request.POST['task_id']
    #(2)テーブルを更新する
    Task.objects.values().filter(id=task_id).update(
        delflg="1"
        )
    #(3)コンテキストを作成
    context = make_context_index()
    return render(request, 'TaskManagement/index.html', context)

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