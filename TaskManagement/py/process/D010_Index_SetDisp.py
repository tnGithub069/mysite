from . import S001_TaskIchrnshtk


#main()メソッドは定型文。正常時、異常時のurlをそれぞれ指定する。
def main(list_msg):
    setDisp_errFlg = "0"
    #一覧の値を取得する
    json_service_S001 = S001_TaskIchrnshtk.main()
    json_TaskList = json_service_S001["json_TaskList"]
    setDisp_errFlg = json_service_S001["flg_result"]
    #実行結果を設定する
    json_setDisp = {'setDisp_errFlg':setDisp_errFlg,'context':json_TaskList}
    return json_setDisp

