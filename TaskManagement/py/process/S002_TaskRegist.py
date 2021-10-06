from ..models import Task

def main(task_title,task_tant,task_kign,task_kihyb,task_detail,task_log,task_status):
    flg_result = "0"
    #(2)テーブルにレコードを作成する
    try:
        Task.objects.create(task_title=task_title,
                            task_tant=task_tant,
                            task_kihyb = task_kihyb,
                            task_kign=task_kign,
                            task_detail=task_detail,
                            task_log=task_log,
                            task_status=task_status,
                            delflg="0",
                            )
    except (KeyError, Task.DoesNotExist):
        flg_result = "1"
        return flg_result
    else:
        return flg_result