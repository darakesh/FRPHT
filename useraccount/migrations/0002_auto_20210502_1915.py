# Generated by Django 3.1.7 on 2021-05-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='drugs',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='medication',
            name='reason',
            field=models.CharField(max_length=200),
        ),
    ]
