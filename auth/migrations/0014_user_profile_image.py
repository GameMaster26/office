# Generated by Django 5.0.6 on 2024-07-22 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0013_user_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='profile_pics'),
        ),
    ]
