# Generated by Django 5.1 on 2024-10-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0009_alter_client_iplinkbackup_alter_client_iplinkmain'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odpId', models.CharField(max_length=100)),
                ('portFilled', models.IntegerField()),
                ('portRemaining', models.IntegerField()),
                ('portOlt', models.CharField(max_length=10)),
                ('oltIp', models.CharField(max_length=20)),
                ('identityOlt', models.CharField(max_length=100)),
                ('Segmen', models.CharField(max_length=100)),
                ('tikor', models.CharField(max_length=255)),
                ('alamat', models.TextField()),
                ('statusOpname', models.CharField(max_length=5)),
                ('remark', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
