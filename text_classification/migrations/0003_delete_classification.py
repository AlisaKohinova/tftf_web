# Generated by Django 4.0.5 on 2022-06-18 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('text_classification', '0002_alter_classification_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Classification',
        ),
    ]
