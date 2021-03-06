# Generated by Django 3.0.8 on 2020-07-28 11:35

from django.db import migrations, models
import django.utils.timezone
import mikroblog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MicroPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, max_length=1500)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.ImageField(blank=True, default='user.png', upload_to=mikroblog.models.upload_location)),
            ],
        ),
    ]
