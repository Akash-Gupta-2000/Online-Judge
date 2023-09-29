from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Problem
from django.contrib.auth.decorators import login_required

@login_required
def getAllProblems(request):
    problems_list = Problem.objects.all()
    problems_dict_list = []
    for problem in problems_list:
        tags = list(problem.tags.all().values())
        problem_dict = model_to_dict(problem)
        problem_dict["tags"] = tags
        problems_dict_list.append(problem_dict)
    # print(problems_dict_list)
    context = {'problems': problems_dict_list}
    return render(request, 'all_problems.html', context)

def getProblemsByPage(request,page_no):
    init_count = (page_no-1)*50;
    problems_list = Problem.objects.all()[init_count:init_count+50]
    problems_dict_list = [model_to_dict(problem) for problem in problems_list]
    return JsonResponse(problems_dict_list, safe=False)

@login_required
def getProblemById(request,id):
    problem = Problem.objects.get(id=id)
    tags = list(problem.tags.all().values())
    problem_dict = model_to_dict(problem)
    problem_dict["tags"] = tags
    print(problem_dict)
    return render(request, 'specific_problem.html', {'problem_data': problem_dict})

