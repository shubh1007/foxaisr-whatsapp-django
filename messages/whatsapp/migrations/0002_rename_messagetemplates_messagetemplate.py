# Generated by Django 4.1.5 on 2023-01-14 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whatsapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MessageTemplates',
            new_name='MessageTemplate',
        ),
    ]
