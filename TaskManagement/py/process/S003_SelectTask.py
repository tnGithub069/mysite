from ..models import Task

def main(task_id):
    flg_result = "0"
    #(2)テーブルにレコードを作成する
    list_one_task = Task.objects.all().filter(id=task_id)
    one_task = list_one_task[0]
    json_service = {"flg_result":flg_result,"one_task":one_task}
    return json_service