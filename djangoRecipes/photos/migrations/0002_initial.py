# Generated by Django 5.1.3 on 2024-11-12 19:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('photos', '0001_initial'),
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipephotos',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='usersphoto',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_picture', to=settings.AUTH_USER_MODEL),
        ),
    ]
