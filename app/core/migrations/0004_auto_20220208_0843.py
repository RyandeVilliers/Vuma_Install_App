# Generated by Django 2.1.15 on 2022-02-08 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_status_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]