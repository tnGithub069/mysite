from ..models import Task

def main():
    flg_result = "0"
    #タスク一覧取得
    all_task_list = Task.objects.filter(delflg="0").order_by('id')
    #json形式に変換
    json_TaskList = {'all_task_list': all_task_list}
    json_service = {"flg_result":flg_result,"json_TaskList":json_TaskList}
    return json_service