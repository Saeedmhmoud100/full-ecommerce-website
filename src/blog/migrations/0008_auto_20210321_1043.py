# Generated by Django 3.1.7 on 2021-03-21 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_blogreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogreview',
            name='reviewimg3',
            field=models.ImageField(default=1, upload_to='blog-review_img'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blogreview',
            name='reviewtitle3',
            field=models.CharField(default=12.24, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogreview',
            name='itemvideourl',
            field=models.CharField(max_length=100),
        ),
    ]
