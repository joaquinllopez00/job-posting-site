# Generated by Django 3.2.5 on 2021-07-10 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20210710_2218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='last_date',
            new_name='post_date',
        ),
    ]
