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
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
>>>>>>> 93547c1e8d82258fb9b37ffebc89802a868a45fe
                ('name', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('phone', models.IntegerField(max_length=10)),
<<<<<<< HEAD
                ('resume', models.FileField(upload_to=b'files/%Y/%m/%d')),
=======
                ('resume', models.FileField(upload_to='files/%Y/%m/%d')),
>>>>>>> 93547c1e8d82258fb9b37ffebc89802a868a45fe
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('areacode', models.PositiveIntegerField(max_length=5)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('trade', models.CharField(max_length=20)),
                ('secondaryTrades', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('pic', models.ImageField(upload_to=b'photos/%Y/%m/%d')),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('areacode', models.PositiveIntegerField(max_length=5)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('primaryTrade', models.CharField(max_length=20)),
                ('secondaryTrades', models.CharField(max_length=200)),
                ('bio', models.TextField()),
                ('pic', models.ImageField(upload_to='photos/%Y/%m/%d')),
>>>>>>> 93547c1e8d82258fb9b37ffebc89802a868a45fe
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContractorSchedule',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('all_day', models.BooleanField(default=False, verbose_name='all day')),
                ('title', models.CharField(max_length=255, verbose_name='title', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
=======
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('all_day', models.BooleanField(default=False, verbose_name='all day')),
                ('title', models.CharField(blank=True, max_length=255, verbose_name='title')),
                ('description', models.TextField(blank=True, verbose_name='description')),
>>>>>>> 93547c1e8d82258fb9b37ffebc89802a868a45fe
                ('firstname', models.ForeignKey(to='zipcode.Contractor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
<<<<<<< HEAD
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
=======
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
>>>>>>> 93547c1e8d82258fb9b37ffebc89802a868a45fe
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contractorschedule',
            name='location',
<<<<<<< HEAD
            field=models.ManyToManyField(to='zipcode.Location', verbose_name='locations', blank=True),
=======
            field=models.ManyToManyField(blank=True, to='zipcode.Location', verbose_name='locations'),
>>>>>>> 93547c1e8d82258fb9b37ffebc89802a868a45fe
            preserve_default=True,
        ),
    ]
