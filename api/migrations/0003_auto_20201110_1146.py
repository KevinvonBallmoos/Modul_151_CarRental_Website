# Generated by Django 3.1.3 on 2020-11-10 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201110_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rent',
            old_name='rend',
            new_name='end',
        ),
    ]
