# Generated by Django 4.1.7 on 2023-03-23 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_djmil', '0002_mainorders_id_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainorders',
            name='id_name',
        ),
    ]