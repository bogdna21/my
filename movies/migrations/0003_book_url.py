# Generated by Django 3.0.3 on 2024-11-25 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20241123_2223'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='url',
            field=models.SlugField(default='duke_and_I', max_length=130, unique=True),
            preserve_default=False,
        ),
    ]
