# Generated by Django 3.0.8 on 2020-08-10 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('mikroblog', '0003_auto_20200731_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='micropost',
            name='tag',
            field=models.ManyToManyField(related_name='micro_posts', to='tag.Tag'),
        ),
    ]