# Generated by Django 3.0.8 on 2020-08-20 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200818_1656'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='imag_url',
            new_name='image_url',
        ),
    ]
