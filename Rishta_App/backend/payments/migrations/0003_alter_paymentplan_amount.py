# Generated by Django 4.0.2 on 2022-05-10 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_paymentplan_currency_alter_paymentplan_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentplan',
            name='amount',
            field=models.IntegerField(default=1000, verbose_name='amount to be charged'),
        ),
    ]
