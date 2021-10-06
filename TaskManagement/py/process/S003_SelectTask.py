from ..models import Task

def main(task_id):
    flg_result = "0"
    #(2)テーブルにレコードを作成する
    list_one_task = Task.objects.all().filter(id=task_id)
    json_service = {"flg_result":flg_result,"list_one_task":list_one_task}
    return json_service