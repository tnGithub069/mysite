from ..models import Task

def main(task_id):
    flg_result = "0"
    #(2)テーブルを更新する
    Task.objects.values().filter(id=task_id).update(
        delflg="1"
        )
    json_service = {"flg_result":flg_result}
    return json_service