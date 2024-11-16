# Generated by Django 5.1.3 on 2024-11-16 13:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('recipes', '0005_alter_recipe_description'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=models.Index(fields=['updated_at'], name='recipes_rec_updated_46db5b_idx'),
        ),
    ]
