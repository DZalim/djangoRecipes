# Generated by Django 5.1.3 on 2024-11-12 19:48

import django.core.validators
import django.db.models.deletion
import djangoRecipes.recipes.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipe_name', models.CharField(error_messages={'unique': 'A recipe with the same name already exists. Please choose another name for your recipe!'}, max_length=100, unique=True)),
                ('difficulty_level', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=10)),
                ('portions', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('preparing_time', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('cooking_time', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('ingredients', models.TextField(validators=[djangoRecipes.recipes.validators.SemicolonValidator()])),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to='categories.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]