# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zipcode', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractor',
            old_name='primaryTrade',
            new_name='trade',
        ),
    ]
