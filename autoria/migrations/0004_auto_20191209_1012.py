# Generated by Django 2.2.8 on 2019-12-09 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoria', '0003_monitorquery_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitorquery',
            name='url',
        ),
        migrations.AddField(
            model_name='monitorquery',
            name='query_string',
            field=models.CharField(default='placeholder', max_length=100),
            preserve_default=False,
        ),
    ]
