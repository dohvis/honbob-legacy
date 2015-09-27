# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='school',
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(null=True, max_length=16),
        ),
    ]
