# Generated by Django 5.1.2 on 2024-11-20 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_contributor_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='desc',
            new_name='description',
        ),
    ]
