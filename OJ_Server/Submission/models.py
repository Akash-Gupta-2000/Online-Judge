from django.db import models
from Problem.models import Problem
from django.contrib.auth.models import User

class Submission(models.Model):
    LANGUAGES = (("C++", "C++"), ("C", "C"), ("Python3", "Python3"),("Java", "Java"))
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    problem_id = models.ForeignKey(Problem, null=True, on_delete=models.SET_NULL)
    user_code = models.TextField(max_length=10000, default="")
    user_stdout = models.TextField(max_length=10000, default="")
    user_stderr = models.TextField(max_length=10000, default="")
    submission_time = models.DateTimeField(auto_now_add=True, null=True)
    run_time = models.FloatField(null=True, default=0)
    language = models.CharField(
        max_length=10, choices=LANGUAGES, default="C++")
    verdict = models.CharField(max_length=100, default="Wrong Answer")
