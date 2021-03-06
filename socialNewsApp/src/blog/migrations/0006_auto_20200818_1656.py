# Generated by Django 3.0.8 on 2020-08-18 16:56

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_post_image_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imag_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=blog.models.upload_location),
        ),
    ]
