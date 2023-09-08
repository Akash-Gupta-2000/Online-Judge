from django.db import models

# Create your models here.

class Tag(models.Model):
    tagname = models.CharField(max_length=20)

class Problem(models.Model):
    problemcode = models.CharField(max_length=20, null=False, unique=True, default='')
    title = models.CharField(max_length=100, null=False, default='', unique=True)
    description = models.TextField(null=False)
    difficulty = models.CharField(null=False, max_length=20)
    score = models.IntegerField(null=False)
    testcases = models.JSONField(null = False ,default = list)
    constraints = models.TextField(null = False, default = '')
    tags = models.ManyToManyField(Tag)

class Testcase(models.Model):
    title = models.CharField(null=False, default='', max_length=50, unique=True)
    input_path = models.TextField(null=False, default='')
    output_path = models.TextField(null=False, default='')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)


