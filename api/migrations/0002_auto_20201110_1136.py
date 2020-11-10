# Generated by Django 3.1.3 on 2020-11-10 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='car_list', to='api.brand'),
        ),
        migrations.AlterField(
            model_name='cars',
            name='image',
            field=models.ImageField(default='noimage.png', upload_to='cars'),
        ),
    ]