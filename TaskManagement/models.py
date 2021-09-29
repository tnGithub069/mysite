"""
参考サイト
■Django モデルフィールド：データベースフィールド 型対応表
https://qiita.com/okoppe8/items/13ad7b7d52fd6a3fd3fc

"""
import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # Questionに対してリレーションを貼る
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Task(models.Model):
    # TASKに対してリレーションを貼る
    task_title = models.CharField(max_length=256)
    task_detail = models.TextField(max_length=10000)
    task_tant = models.CharField(max_length=64)
    task_log = models.TextField(max_length=10000)
    task_kihyb = models.DateTimeField('date published')
    task_kign =  models.DateTimeField('date published')
    task_status = models.CharField(max_length=32)
    delflg = models.CharField(max_length=1)
    def __str__(self):
        return self.task_title