# Generated by Django 4.0.5 on 2022-11-29 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '00010_thisweekitem_nextweekitem_move_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='next_week',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='this_week',
        ),
    ]
