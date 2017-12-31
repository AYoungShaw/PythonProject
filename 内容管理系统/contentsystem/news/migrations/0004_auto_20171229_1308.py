# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20171229_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='column',
            name='home_display',
        ),
        migrations.RemoveField(
            model_name='column',
            name='nav_display',
        ),
    ]
