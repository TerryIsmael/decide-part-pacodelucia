# Generated by Django 4.1 on 2023-12-14 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
        ('visualizer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stats',
            options={},
        ),
        migrations.RemoveField(
            model_name='stats',
            name='name',
        ),
        migrations.AddField(
            model_name='stats',
            name='voting',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='voting.voting'),
        ),
    ]
