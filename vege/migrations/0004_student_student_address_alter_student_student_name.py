# Generated by Django 5.0.6 on 2024-07-05 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0003_department_studentid_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_address',
            field=models.TextField(default='Unknown address'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_name',
            field=models.CharField(max_length=100),
        ),
    ]
