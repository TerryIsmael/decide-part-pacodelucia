
# Generated by Django 4.1 on 2023-12-15 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='census',
            name='census_group',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]