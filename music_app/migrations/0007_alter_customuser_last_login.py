# Generated by Django 5.1.3 on 2025-02-02 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0006_customuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
