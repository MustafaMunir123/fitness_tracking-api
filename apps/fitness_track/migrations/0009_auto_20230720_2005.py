# Generated by Django 3.2.5 on 2023-07-20 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_track', '0008_alter_customuser_complete_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userexercise',
            name='done',
        ),
        migrations.AlterField(
            model_name='userexercise',
            name='last_attempt',
            field=models.DateField(auto_now=True),
        ),
    ]