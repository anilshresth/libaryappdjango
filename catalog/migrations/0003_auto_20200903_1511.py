# Generated by Django 3.0.6 on 2020-09-03 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20200903_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'set_book_as_returned'),)},
        ),
    ]