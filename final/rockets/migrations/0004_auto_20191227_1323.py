# Generated by Django 2.1.5 on 2019-12-27 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rockets', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
