from . import S003_SelectTask


#main()メソッドは定型文。正常時、異常時のurlをそれぞれ指定する。
def main(list_msg):
    setDisp_errFlg = "0"
    #システム日時を取得
    today = datetime.datetime.now()
    today = format(today, '%Y-%m-%d')
    #コンテキストを作成
    context = {'today':today}
    json_setDisp = {'setDisp_errFlg':setDisp_errFlg,'context':context}
    return json_setDisp

