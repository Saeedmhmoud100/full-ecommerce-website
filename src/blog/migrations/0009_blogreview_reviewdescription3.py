# Generated by Django 3.1.7 on 2021-03-21 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210321_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogreview',
            name='reviewdescription3',
            field=models.TextField(default=12163),
            preserve_default=False,
        ),
    ]
