# Generated by Django 2.2.8 on 2019-12-08 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoria', '0002_auto_20191207_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorquery',
            name='url',
            field=models.URLField(default='http://nothing.com'),
            preserve_default=False,
        ),
    ]
