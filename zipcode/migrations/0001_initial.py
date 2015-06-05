# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CareerResume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.IntegerField(max_length=10)),
                ('resume', models.FileField(upload_to=b'files/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('areacode', models.PositiveIntegerField(max_length=5)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('trade', models.CharField(max_length=20)),
                ('secondaryTrades', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('pic', models.ImageField(upload_to=b'photos/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractorSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('all_day', models.BooleanField(default=False, verbose_name='all day')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('firstname', models.ForeignKey(to='zipcode.Contractor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.FileField(upload_to=b'gallery/%Y/%m/%d')),
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
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address_line_1', models.CharField(max_length=255, verbose_name='Address Line 1', blank=True)),
                ('address_line_2', models.CharField(max_length=255, verbose_name='Address Line 2', blank=True)),
                ('address_line_3', models.CharField(max_length=255, verbose_name='Address Line 3', blank=True)),
                ('state', models.CharField(max_length=63, verbose_name='State / Province / Region', blank=True)),
                ('city', models.CharField(max_length=63, verbose_name='City / Town', blank=True)),
                ('zipcode', models.CharField(max_length=31, verbose_name='ZIP / Postal Code', blank=True)),
                ('country', models.CharField(max_length=127, verbose_name='Country', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_name', models.CharField(max_length=255, verbose_name='customer name', blank=True)),
                ('customer_city', models.CharField(max_length=255, verbose_name='customer city', blank=True)),
                ('customer_testimonial', models.TextField(max_length=255, verbose_name='customer testimonial', blank=True)),
                ('customer_date', models.DateTimeField(verbose_name='customer date')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contractorschedule',
            name='location',
            field=models.ManyToManyField(to='zipcode.Location', verbose_name='locations', blank=True),
            preserve_default=True,
        ),
    ]
