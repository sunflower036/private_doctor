# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-06-10 11:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('private_doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Family_Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateField(auto_created=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='private_doctor.Doctor')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='private_doctor.Family')),
            ],
        ),
    ]
