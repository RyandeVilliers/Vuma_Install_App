# Generated by Django 2.1.15 on 2022-03-06 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220305_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[('Installation Requested', 'Installation Requested'), ('Installation in Progress', 'Installation in Progress'), ('Installation Complete', 'Installation Complete'), ('Installation Rejected', 'Installation Rejected')], default='Installation Requested', max_length=255),
        ),
    ]
