# Generated by Django 4.0 on 2022-09-20 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default='default_profile_pic.jpg', upload_to=''),
        ),
    ]
