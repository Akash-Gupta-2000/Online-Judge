# Generated by Django 4.2.4 on 2023-09-17 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Problem', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='difficulty',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Tough', 'Tough')], max_length=20),
        ),
    ]