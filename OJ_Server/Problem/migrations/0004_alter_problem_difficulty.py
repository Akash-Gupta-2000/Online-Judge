# Generated by Django 4.2.4 on 2023-09-17 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Problem', '0003_remove_problem_score_remove_problem_testcases'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=20),
        ),
    ]
