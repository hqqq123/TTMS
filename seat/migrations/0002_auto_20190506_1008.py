# Generated by Django 2.1.7 on 2019-05-06 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='studio_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studio.Studio'),
        ),
    ]
