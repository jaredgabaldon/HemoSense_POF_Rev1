# Generated by Django 2.2.7 on 2019-11-29 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20191127_1622'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(help_text='Enter a brief description of the book', max_length=1000)),
                ('isbn', models.CharField(help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=13, verbose_name='ISBN')),
                ('person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Author')),
                ('type_of_injury', models.ManyToManyField(help_text='Select a genre for this book', to='catalog.Genre')),
            ],
        ),
    ]
