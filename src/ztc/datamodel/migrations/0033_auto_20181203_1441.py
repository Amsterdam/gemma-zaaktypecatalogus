# Generated by Django 2.0.8 on 2018-12-03 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0032_auto_20181029_1037'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='roltype',
            unique_together={('zaaktype', 'omschrijving')},
        ),
    ]
