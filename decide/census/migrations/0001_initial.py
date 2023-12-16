# Generated by Django 4.1 on 2023-12-12 13:24


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Census',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_id', models.PositiveIntegerField()),
                ('voter_id', models.PositiveIntegerField()),
                ('born_year', models.PositiveIntegerField(null=True)),
                ('country', models.CharField(max_length=50, null=True)),
                ('religion', models.CharField(choices=[('CH', 'Christianity'), ('IS', 'Islamism'), ('HI', 'Hinduism'), ('BU', 'Buddhism'), ('AG', 'Agnosticism'), ('AT', 'Atheism'), ('OT', 'Other')], max_length=2, null=True)),
                ('gender', models.CharField(choices=[('MA', 'Male'), ('FE', 'Female'), ('NB', 'Non binary'), ('NP', 'No response')], max_length=2, null=True)),
                ('civil_state', models.CharField(choices=[('SI', 'Single'), ('MA', 'Married'), ('DI', 'Divorced'), ('WI', 'Widower')], max_length=2, null=True)),
                ('works', models.CharField(choices=[('ST', 'Student'), ('WO', 'Worker'), ('UN', 'Unemployed')], max_length=2, null=True)),
            ],
            options={
                'unique_together': {('voting_id', 'voter_id', 'born_year', 'gender', 'civil_state', 'works')},
            },
        ),
    ]
