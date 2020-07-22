# Generated by Django 3.0.8 on 2020-07-22 18:43

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200714_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='background',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.upload_location),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='user.png', upload_to=user.models.upload_location),
        ),
    ]