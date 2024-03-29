# Generated by Django 2.2.7 on 2019-12-09 00:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_auto_20191208_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='bleedinfo',
            name='extra_factor_yn',
            field=models.IntegerField(choices=[(1, 'Yes'), (2, 'No')], default=1),
        ),
        migrations.AddField(
            model_name='bleedinfo',
            name='when_bleed_occured',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
