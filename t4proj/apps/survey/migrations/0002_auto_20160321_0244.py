# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='rank',
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='survey.Question'),
        ),
        migrations.AlterField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(null=True, related_name='responses', to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='response',
            name='room',
            field=models.ForeignKey(default=None, related_name='responses', to='survey.Room'),
            preserve_default=False,
        ),
    ]
