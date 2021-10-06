from . import S003_SelectTask


#main()メソッドは定型文。正常時、異常時のurlをそれぞれ指定する。
def main(list_msg,task_id):
    setDisp_errFlg = "0"
    #1課題取得サービスを呼び出し、課題情報を取得する
    json_service = S003_SelectTask.main(task_id)
    list_one_task = json_service["list_one_task"]
    #表示用の期限日のフォーマットを整える
    hyoji_kigen = list_one_task[0].task_kign
    hyoji_kigen = format(hyoji_kigen, '%Y-%m-%d')
    #コンテキストを作成
    context = {'list_one_task': list_one_task,
                'hyoji_kigen': hyoji_kigen,
                }
    json_setDisp = {'setDisp_errFlg':setDisp_errFlg,'context':context}
    return json_setDisp

