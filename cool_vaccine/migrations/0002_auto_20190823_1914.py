# Generated by Django 2.2.4 on 2019-08-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cool_vaccine', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GP',
            new_name='GP_Info',
        ),
        migrations.AlterField(
            model_name='vaccine_compare',
            name='vaccine_time',
            field=models.IntegerField(verbose_name=3),
        ),
    ]
