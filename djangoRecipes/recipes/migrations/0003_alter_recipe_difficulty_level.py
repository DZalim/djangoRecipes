# Generated by Django 5.1.3 on 2024-11-12 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_difficulty_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='difficulty_level',
            field=models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=10),
        ),
    ]
