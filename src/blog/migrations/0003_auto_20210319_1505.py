# Generated by Django 3.1.7 on 2021-03-19 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_postcomment_pcomtitle'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='post',
            name='PostImg',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='blog_images'),
        ),
    ]