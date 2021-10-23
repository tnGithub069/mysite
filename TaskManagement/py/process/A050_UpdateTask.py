import datetime
from . import C010_Const
from . import S003_SelectTask,S004_UpdateTask


#main()メソッドは定型文。正常時、異常時のtemplateをそれぞれ指定する。
def main(request,list_msg):
    template = ""
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
            list_msg.append({"level":C010_Const.SUCCESS,"msg":"更新が完了しました。"})
            #正常時の遷移先
            template = "TaskManagement/detail_task.html"
        else:
            #flw処理で業務エラーありの場合
            #エラー時の遷移先
            template = "TaskManagement/detail_task.html"
            list_msg.append({"level":C010_Const.ERROR,"msg":"更新に失敗しました。"})
    else:
        #入力エラー時の遷移先
        template = "TaskManagement/detail_task.html"
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
    json_service_S004 = S004_UpdateTask.main(task_id,task_title,task_tant,task_kign,task_kihyb,task_detail,task_log,task_status)
    flw_errFlg = json_service_S004["flg_result"]
    #表示処理------------------------------------------------------
    #(3)更新後の値を取得する
    json_service_S003 = S003_SelectTask.main(task_id)
    one_task = json_service_S003["one_task"]
    flw_errFlg = json_service_S003["flg_result"]
    #(4)表示期限を取得
    hyoji_kigen = one_task.task_kign
    hyoji_kigen = format(hyoji_kigen, '%Y-%m-%d')
    #(5)コンテキストを作成
    context = {'task': one_task,
                'hyoji_kigen': hyoji_kigen,
                }
    #検証--------------------------------------------------------------------
    json_msg1={"level":C010_Const.DEBUG,"msg":"更新しました１"}
    json_msg2={"level":C010_Const.INFO,"msg":"更新しました２"}
    json_msg3={"level":C010_Const.SUCCESS,"msg":"更新しました３"}
    json_msg4={"level":C010_Const.WARNING,"msg":"更新しました４"}
    json_msg5={"level":C010_Const.ERROR,"msg":"更新しました５"}
    list_msg.append(json_msg1)
    list_msg.append(json_msg2)
    list_msg.append(json_msg3)
    list_msg.append(json_msg4)
    list_msg.append(json_msg5)
    #検証--------------------------------------------------------------------

    #実行結果を設定する
    json_flw = {'flw_errFlg':flw_errFlg,'context':context}
    #表示処理------------------------------------------------------
    return json_flw