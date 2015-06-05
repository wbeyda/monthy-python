# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zipcode', '0002_auto_20150514_0016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('picture', models.FileField(upload_to='gallery/%Y/%m/%d')),
                ('caption', models.CharField(max_length=255, verbose_name='caption', blank=True)),
                ('author', models.CharField(max_length=255, verbose_name='author', blank=True)),
                ('sourceURL', models.URLField(verbose_name='source URL', blank=True)),
                ('picdate', models.DateTimeField(verbose_name='pic date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('customer_name', models.CharField(max_length=255, verbose_name='customer name', blank=True)),
                ('customer_city', models.CharField(max_length=255, verbose_name='customer city', blank=True)),
                ('customer_testimonial', models.TextField(max_length=255, verbose_name='customer testimonial', blank=True)),
                ('customer_date', models.DateTimeField(verbose_name='customer date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
