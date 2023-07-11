# Generated by Django 3.2.5 on 2023-07-11 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_track', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_name', models.CharField(blank=True, max_length=50)),
                ('burn_calories', models.PositiveIntegerField(blank=True)),
                ('sets', models.PositiveIntegerField(default=3, null=True)),
                ('reps', models.PositiveIntegerField(default=3, null=True)),
                ('last_attempted', models.DateField(blank=True, null=True)),
                ('done', models.BooleanField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(blank=True)),
                ('weight', models.FloatField(blank=True)),
                ('sleep', models.FloatField(blank=True)),
                ('walk', models.FloatField(blank=True, null=True)),
                ('exercises', models.ManyToManyField(related_name='user_details', to='fitness_track.UserExercise')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, choices=[('Fat Loss', 'FAT_LOSS')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goal', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_history', to='fitness_track.userexercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_history', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
