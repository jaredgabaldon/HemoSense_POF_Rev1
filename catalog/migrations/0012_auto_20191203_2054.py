# Generated by Django 2.2.7 on 2019-12-04 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_injury_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='injury',
            name='type_of_injury',
        ),
        migrations.AddField(
            model_name='injury',
            name='type_of_injury',
            field=models.IntegerField(choices=[(1, 'Not relevant'), (2, 'Review'), (3, 'Maybe relevant'), (4, 'Relevant'), (5, 'Leading candidate')], default=1),
        ),
    ]
