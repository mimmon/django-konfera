# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-16 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import konfera.models.speaker


class Migration(migrations.Migration):

    dependencies = [
        ('konfera', '0032_auto_20170202_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='image',
            field=models.ImageField(blank=True, upload_to=konfera.models.speaker.img_path),
        ),
    ]