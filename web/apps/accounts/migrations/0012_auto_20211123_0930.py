# Generated by Django 3.2.9 on 2021-11-23 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20211123_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='multiaccounts',
            name='credit_card_field',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='multiaccounts',
            name='first_last_field',
            field=models.CharField(max_length=15),
        ),
    ]