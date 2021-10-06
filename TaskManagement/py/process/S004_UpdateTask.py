from ..models import Task

def main(task_id,task_title,task_tant,task_kign,task_kihyb,task_detail,task_log,task_status):
    flg_result = "0"
    #Store.objects.values().filter(name__istartswith='st').update(registered_users=F('registered_users') + 1)
    Task.objects.values().filter(id=task_id).update(
        task_title = task_title,
        task_tant = task_tant,
        task_kign = task_kign,
        task_kihyb = task_kihyb,
        task_detail = task_detail,
        task_log = task_log,
        task_status = task_status,
        )
    json_service = {"flg_result":flg_result}
    return json_service