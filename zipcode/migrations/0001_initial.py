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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.IntegerField(max_length=10)),
                ('resume', models.FileField(upload_to='files/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('areacode', models.PositiveIntegerField(max_length=5)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('primaryTrade', models.CharField(max_length=20)),
                ('secondaryTrades', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('pic', models.ImageField(upload_to='photos/%Y/%m/%d')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractorSchedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('all_day', models.BooleanField(default=False, verbose_name='all day')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('firstname', models.ForeignKey(to='zipcode.Contractor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('address_line_1', models.CharField(blank=True, max_length=255, verbose_name='Address Line 1')),
                ('address_line_2', models.CharField(blank=True, max_length=255, verbose_name='Address Line 2')),
                ('address_line_3', models.CharField(blank=True, max_length=255, verbose_name='Address Line 3')),
                ('state', models.CharField(blank=True, max_length=63, verbose_name='State / Province / Region')),
                ('city', models.CharField(blank=True, max_length=63, verbose_name='City / Town')),
                ('zipcode', models.CharField(blank=True, max_length=31, verbose_name='ZIP / Postal Code')),
                ('country', models.CharField(blank=True, max_length=127, verbose_name='Country')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contractorschedule',
            name='location',
            field=models.ManyToManyField(blank=True, to='zipcode.Location', verbose_name='locations'),
            preserve_default=True,
        ),
    ]
