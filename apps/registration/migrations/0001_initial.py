# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-20 01:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote_by', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=255)),
                ('birthdate', models.DateTimeField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='quote',
            name='faved_by',
            field=models.ManyToManyField(blank=True, null=True, related_name='favquotes', to='registration.User'),
        ),
        migrations.AddField(
            model_name='quote',
            name='posted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poster', to='registration.User'),
        ),
    ]
