# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('img', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('url', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=128, null=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('rate', models.IntegerField()),
                ('comment', models.CharField(max_length=500)),
                ('Restaurant', models.ForeignKey(to='restaurant.Restaurant', related_name='reviews')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='recently_visit')),
            ],
        ),
        migrations.AddField(
            model_name='links',
            name='Restaurant',
            field=models.ForeignKey(to='restaurant.Restaurant', related_name='links'),
        ),
        migrations.AddField(
            model_name='images',
            name='link',
            field=models.ForeignKey(to='restaurant.Links', related_name='images'),
        ),
    ]
