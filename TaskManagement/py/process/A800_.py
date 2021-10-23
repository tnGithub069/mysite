import datetime
from . import C010_Const
from . import S001_TaskIchrnshtk,S005_DeleteTask_logical


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
            list_msg.append({"level":C010_Const.SUCCESS,"msg":"削除が完了しました。"})
            #正常時の遷移先
            template = "TaskManagement/index.html"
        else:
            #flw処理で業務エラーありの場合
            #エラー時の遷移先
            template = "TaskManagement/detail_task.html"
            list_msg.append({"level":C010_Const.ERROR,"msg":"削除に失敗しました。"})
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
    #(1)画面パラメータから削除所対象のPkeyを取得する
    task_id = request.POST['task_id']
    #(2)テーブルを更新する
    json_service_S005 = S005_DeleteTask_logical.main(task_id)
    flw_errFlg = json_service_S005["flg_result"]
    #表示処理------------------------------------------------------
    #(3)一覧の値を取得する
    json_service_S001 = S001_TaskIchrnshtk.main()
    json_TaskList = json_service_S001["json_TaskList"]
    flw_errFlg = json_service_S001["flg_result"]
    #実行結果を設定する
    json_flw = {'flw_errFlg':flw_errFlg,'context':json_TaskList}
    #表示処理------------------------------------------------------
    return json_flw