# Generated by Django 2.1.5 on 2019-02-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='next_week',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recipe',
            name='this_week',
            field=models.BooleanField(default=False),
        ),
    ]
