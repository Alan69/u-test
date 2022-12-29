# Generated by Django 4.1.1 on 2022-12-28 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizes', '0005_alter_quiz_required_score_to_pass_alter_quiz_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='grade',
        ),
        migrations.AddField(
            model_name='quiz',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='quizes.grade'),
        ),
    ]
