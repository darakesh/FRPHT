# Generated by Django 3.1.7 on 2021-05-03 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210502_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='userID',
            field=models.CharField(max_length=8, primary_key=True, serialize=False, unique=True),
        ),
    ]
