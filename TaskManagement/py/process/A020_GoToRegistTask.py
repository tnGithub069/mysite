import datetime
from . import S006_GetKeibaNews

#main()メソッドは定型文。正常時、異常時のtemplateをそれぞれ指定する。
def main(request,list_msg):
    template = ""
    #preメソッドを実行
    context = pre(request,list_msg)
    #入力チェックOK(checkFlg == 0)の場合、flwメソッドを実行
    if context["commonItem_checkFlg"] == "0":
        json_flw = flw(request,list_msg)
        flw_context = json_flw["context"]
        context = {**context,**flw_context}
        #正常時の遷移先
        template = "TaskManagement/regist_task.html"
    else:
        #入力エラー時の遷移先
        template = "TaskManagement/regist_task.html"
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
    #サービスの呼び出しなし
    #表示処理------------------------------------------------------
    today = datetime.datetime.now()
    today = format(today, '%Y-%m-%d')
    list_newsInfo = S006_GetKeibaNews.main(10)
    context = {'today':today,"list_newsInfo":list_newsInfo}
    json_flw = {'flw_errFlg':flw_errFlg,'context':context}
    #表示処理------------------------------------------------------
    return json_flw