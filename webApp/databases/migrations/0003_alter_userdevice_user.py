# Generated by Django 5.1 on 2024-09-17 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0002_rename_userdevicemodel_userdevice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdevice',
            name='user',
            field=models.CharField(choices=[('', 'admin'), ('', 'deni'), ('', 'randi'), ('', 'fitria'), ('', 'farros'), ('', 'yazid')], default='admin', max_length=100),
        ),
    ]
