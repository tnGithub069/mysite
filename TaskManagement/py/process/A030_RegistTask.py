import datetime
from django.urls import reverse
from . import S001_TaskIchrnshtk,S002_TaskRegist
from . import C010_Const



#main()メソッドは定型文。正常時、異常時のtemplateをそれぞれ指定する。
def main(request,list_msg):
    template = "TaskManagement/regist_task.html"
    context = {}
    #preメソッドを実行
    context = pre(request,list_msg)
    #入力チェックOK(checkFlg == 0)の場合、flwメソッドを実行
    if context["commonItem_checkFlg"] == "0":
        json_flw = flw(request,list_msg)
        if json_flw['flw_errFlg'] == "0":
            #flw処理で業務エラーなしの場合
            flw_context =  json_flw['context']
            context = {**context,**flw_context}
            #正常終了メッセージ
            list_msg.append({"level":C010_Const.SUCCESS,"msg":"登録完了しました。"})
            #正常時の遷移先
            template = "TaskManagement/index.html"
            url = reverse("TaskManagement:index")
            success_url = url
        else:
            #flw処理で業務エラーありの場合
            #エラー時の遷移先
            template = "TaskManagement/regist_task.html"
            list_msg.append({"level":C010_Const.ERROR,"msg":"登録に失敗しました。"})
    else:
        #入力エラー時の遷移先
        template = "TaskManagement/regist_task.html"
        list_msg.append({"level":C010_Const.ERROR,"msg":"入力に誤りがあります"})
    #戻り値を設定
    json_main = {'context':context, 'template':template}
    return json_main

#pre()は入力チェック用メソッド。check結果：NGの場合はビジネスエラーを返す。
def pre(request,list_msg):
    check_flg = "0"
    json_pre = {"commonItem_checkFlg":check_flg}
    return json_pre

#flw()は業務処理用メソッド。入力チェックが正常に終了した場合、処理を実施する。サービスを呼び出したりする。
def flw(request,list_msg):
    flw_errFlg = "0"
    #サービスの引数をリクエストから取得する
    task_title = request.POST['task_title']
    task_tant = request.POST['task_tant']
    task_kign = request.POST['task_kign']
    task_kihyb = datetime.datetime.now()
    task_detail = request.POST['task_detail']
    task_log = request.POST['task_log']
    task_status = request.POST['task_status']
    #サービスを呼び出す
    flw_errFlg = S002_TaskRegist.main(task_title,task_tant,task_kign,task_kihyb,task_detail,task_log,task_status)
    #一覧用コンテキストを作成
    #表示処理------------------------------------------------------
    #(3)一覧の値を取得する
    json_service_S001 = S001_TaskIchrnshtk.main()
    json_TaskList = json_service_S001["json_TaskList"]
    flw_errFlg = json_service_S001["flg_result"]
    #実行結果を設定する
    json_flw = {'flw_errFlg':flw_errFlg,'context':json_TaskList}
    #表示処理------------------------------------------------------
    return json_flw