# Generated by Django 5.1 on 2024-10-20 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0016_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='watt',
            field=models.FloatField(default=0),
        ),
    ]