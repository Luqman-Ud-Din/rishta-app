# Generated by Django 4.0.2 on 2022-04-29 18:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='detail',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='detail'),
        ),
    ]
