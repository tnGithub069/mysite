from . import S001_TaskIchrnshtk,D010_Index_SetDisp,S006_GetKeibaNews


#main()メソッドは定型文。正常時、異常時のtemplateをそれぞれ指定する。
def main(request,list_msg):
    template = ""
    #preメソッドを実行
    context = {}
    json_pre = pre(request,list_msg)
    context = {**context,**json_pre["context"]}
    #入力チェックOK(checkFlg == 0)の場合、flwメソッドを実行
    if json_pre["pre_errFlg"] == "0":
        json_flw = flw(request,list_msg)
        context = {**context,**json_flw["context"]}
        if json_flw["flw_errFlg"] == "0":
            #flwクラス正常終了の場合
            #表示クラスを呼び出し、表示用のコンテキストを作成する
            json_setDisp = D010_Index_SetDisp.main(list_msg)
            if json_setDisp["setDisp_errFlg"] == "0":
                context = {**context,**json_setDisp["context"]}
                #正常時の遷移先
                template = "TaskManagement/index.html"
            else:
                template = "TaskManagement/err500.html"
        else:
            template = "TaskManagement/index.html"
    else:
        #入力エラー時の遷移先
        template = "TaskManagement/index.html"
    #戻り値を設定
    json_main = {'context':context, 'template':template}
    return json_main

#pre()は入力チェック用メソッド。check結果：NGの場合はビジネスエラーを返す。
def pre(request,list_msg):
    pre_errFlg = "0"
    context = {}
    json_pre = {"pre_errFlg":pre_errFlg,"context":context}
    return json_pre

#flw()は業務処理用メソッド。入力チェックが正常に終了した場合、処理を実施する。サービスを呼び出したりする。
def flw(request,list_msg):
    flw_errFlg = "0"
    list_newsInfo = S006_GetKeibaNews.main(0)
    context = {"list_newsInfo":list_newsInfo}
    json_flw = {"flw_errFlg":flw_errFlg,"context":context}
    return json_flw
