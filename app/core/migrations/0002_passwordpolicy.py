# Generated by Django 2.1.15 on 2021-01-13 13:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('min_length', models.IntegerField()),
                ('min_characters', models.IntegerField()),
                ('min_lowercase', models.IntegerField()),
                ('min_uppercase', models.IntegerField()),
                ('min_special_char', models.IntegerField()),
                ('min_different_char', models.IntegerField()),
                ('max_consecutive_char', models.IntegerField()),
                ('max_consecutive_char_type', models.IntegerField()),
                ('exp_interval', models.IntegerField(default=90)),
                ('warn_interval', models.IntegerField()),
                ('pwd_history', models.IntegerField(default=7)),
                ('is_alpha_numeric', models.BooleanField(default=True)),
                ('allow_username', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
