# Generated by Django 2.0.8 on 2018-09-11 08:19
import uuid

from django.db import migrations


def set_uuid(apps, _):
    BesluitType = apps.get_model('datamodel', 'BesluitType')
    for besluittype in BesluitType.objects.all():
        besluittype.uuid = uuid.uuid4()
        besluittype.save()


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0029_besluittype_uuid'),
    ]

    operations = [
        migrations.RunPython(set_uuid, migrations.RunPython.noop),
    ]