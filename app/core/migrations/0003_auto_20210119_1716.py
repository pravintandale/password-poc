# Generated by Django 3.1 on 2021-01-19 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210119_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordpolicy',
            name='max_consecutive_char',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='passwordpolicy',
            name='max_consecutive_char_type',
            field=models.IntegerField(default=5),
        ),
    ]
