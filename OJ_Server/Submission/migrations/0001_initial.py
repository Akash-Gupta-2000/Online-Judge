# Generated by Django 4.2.4 on 2023-09-26 18:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Problem', '0004_alter_problem_difficulty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.TextField(default='', max_length=10000)),
                ('user_stdout', models.TextField(default='', max_length=10000)),
                ('user_stderr', models.TextField(default='', max_length=10000)),
                ('submission_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('run_time', models.FloatField(default=0, null=True)),
                ('language', models.CharField(choices=[('C++', 'C++'), ('C', 'C'), ('Python3', 'Python3'), ('Java', 'Java')], default='C++', max_length=10)),
                ('verdict', models.CharField(default='Wrong Answer', max_length=100)),
                ('problem_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Problem.problem')),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
