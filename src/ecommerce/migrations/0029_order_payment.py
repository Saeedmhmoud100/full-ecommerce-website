# Generated by Django 3.1.7 on 2021-04-04 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0028_auto_20210404_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
