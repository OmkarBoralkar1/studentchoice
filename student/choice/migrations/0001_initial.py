# Generated by Django 3.2 on 2024-01-01 11:59

import choice.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=choice.models.get_file_path)),
                ('start_row', models.IntegerField()),
                ('end_row', models.IntegerField()),
                ('start_column', models.IntegerField()),
                ('end_column', models.IntegerField()),
            ],
        ),
    ]
