# Generated by Django 3.0.3 on 2020-03-02 04:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0002_goalchallenge'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_completed', models.IntegerField(default=0)),
                ('misess_remaining', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('goal_challenge', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goals.GoalChallenge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
