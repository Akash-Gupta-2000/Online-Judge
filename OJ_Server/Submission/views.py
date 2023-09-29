from django.shortcuts import render
import docker
from Problem.models import Problem, Testcase
from .models import Submission
from django.contrib.auth.models import User
import subprocess
import os
from time import time
from django.conf import settings
from datetime import datetime

def verdict(request, problem_id):
    if request.method == 'POST':
        problem = Problem.objects.get(id = problem_id)
        testcase = Testcase.objects.get(problem_id = problem_id)
        verdict, run_time  = "Wrong Answer", 0

        # Extract Data from Form
        language = request.POST.get('language', '')  # Get the selected language
        user_code = request.POST.get('user_code', '')  # Get the user's code
        user_code = user_code.replace('\r\n', '\n').strip()
        print(f"Language: {language}")
        print(f"User Code: {user_code}")
        submission = Submission(user=request.user, problem=problem, submission_time=datetime.now(), 
                                    language=language, user_code=user_code)
        submission.save()
        filename = str(submission.id)

        # Replacing all occurrences of the Windows-style newline characters (\r\n) with 
        # Unix-style newline characters (\n)
        testcase.output = testcase.output.replace('\r\n','\n').strip() 
        
        # if user code is in C++
        if language == "C++":
            extension = ".cpp"
            cont_name = "oj-cpp"
            compile = f"g++ -o {filename} {filename}.cpp"
            clean = f"{filename} {filename}.cpp"
            docker_img = "gcc"
            exe = f"./{filename}"
            
        elif language == "C":
            extension = ".c"
            cont_name = "oj-c"
            compile = f"gcc -o {filename} {filename}.c"
            clean = f"{filename} {filename}.c"
            docker_img = "gcc"
            exe = f"./{filename}"

        elif language == "Python":
            extension = ".py"
            cont_name = "oj-py3"
            compile = "python3"
            clean = f"{filename}.py"
            docker_img = "python"
            exe = f"python {filename}.py"
        
        file = filename + extension
        filepath = os.path.join(settings.FILES_DIR, file)

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as code:
            code.write(user_code)
        print("Local File Path: ", filepath)
        
        try:
            docker_client = docker.from_env()
            container = docker_client.containers.get(cont_name)
            container_state = container.attrs['State']

            # Check if the container is not running, then start it
            if not container_state['Status'] == "running":
                subprocess.run(f"docker start {cont_name}",shell=True)

        except docker.errors.NotFound:
            # If the container doesn't exist, create and run it
            subprocess.run(f"docker run -dt --name {cont_name} {docker_img}",shell=True)

        # copy/paste the Code file in docker container 
        # print(f"docker cp {filepath} {cont_name}:/{file}")
        subprocess.run(f"docker cp {filepath} {cont_name}:/{file}",shell=True)

        # compiling the code
        cmp = subprocess.run(f"docker exec {cont_name} {compile}", capture_output=True, shell=True)
        # print(f"docker exec {cont_name} {compile}")
        print(cmp)
        if cmp.returncode != 0:
            verdict = "Compilation Error"
            subprocess.run(f"docker exec {cont_name} rm {file}",shell=True)

        else:
            # running the code on given input and taking the output in a variable in bytes
            start = time()
            try:
                res = subprocess.run(f'''docker exec {cont_name} sh -c "echo '{testcase.input}' | {exe}"''',
                                                capture_output=True, timeout=1, shell=True)
                # print(f"docker exec {cont_name} sh -c 'echo \"{testcase.input}\" | {exe}'")
                run_time = time()-start
                subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)
                print(res)
            except subprocess.TimeoutExpired:
                run_time = time()-start
                verdict = "Time Limit Exceeded"
                subprocess.run(f"docker container kill {cont_name}", shell=True)
                subprocess.run(f"docker start {cont_name}",shell=True)
                subprocess.run(f"docker exec {cont_name} rm {clean}",shell=True)

            if verdict != "Time Limit Exceeded" and res.returncode != 0:
                verdict = "Runtime Error"
                

        user_stderr = ""
        user_stdout = ""
        if verdict == "Compilation Error":
            user_stderr = cmp.stderr.decode('utf-8')
        
        elif verdict == "Wrong Answer":
            user_stdout = res.stdout.decode('utf-8')
            if user_stdout == testcase.output:
                verdict = "Accepted"
            # Add an extra line to compare user output having an extra line at the end of their output
            if user_stdout == testcase.output + '\n':
                verdict = "Accepted"

        submission.verdict = verdict
        submission.user_stdout = user_stdout
        submission.user_stderr = user_stderr
        submission.run_time = run_time
        submission.save()
        os.remove(filepath)

        context = {
            'verdict': verdict,
            'verdict_css_class': 'accepted' if verdict == 'Accepted' else 'wrong-answer' if verdict == 'Wrong Answer' else 'other'
        }
        return render(request,'verdict.html',context)
