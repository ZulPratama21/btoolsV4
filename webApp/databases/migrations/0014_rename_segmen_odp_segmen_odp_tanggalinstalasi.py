# Generated by Django 5.1 on 2024-10-16 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0013_alter_odp_statusopname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='odp',
            old_name='Segmen',
            new_name='segmen',
        ),
        migrations.AddField(
            model_name='odp',
            name='tanggalinstalasi',
            field=models.DateField(default='2024-10-17'),
            preserve_default=False,
        ),
    ]