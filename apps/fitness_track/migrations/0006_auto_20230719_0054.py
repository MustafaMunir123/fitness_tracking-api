# Generated by Django 3.2.5 on 2023-07-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_track', '0005_alter_userexercise_last_attempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='user',
        ),
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]