# Generated by Django 3.0.8 on 2020-08-10 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('mikroblog', '0004_auto_20200810_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micropost',
            name='tag',
            field=models.ManyToManyField(to='tag.Tag'),
        ),
    ]