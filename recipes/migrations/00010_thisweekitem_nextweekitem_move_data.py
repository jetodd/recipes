from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_thisweekitem_nextweekitem'),
    ]

    operations = [
        migrations.RunSQL(
            'INSERT INTO recipes_thisweekitem ( recipe_id, "position" ) SELECT id, 0 FROM recipes_recipe WHERE this_week = true;'
        ),
        migrations.RunSQL(
            'INSERT INTO recipes_nextweekitem ( recipe_id, "position" ) SELECT id, 0 FROM recipes_recipe WHERE next_week = true;'
        ),
    ]
