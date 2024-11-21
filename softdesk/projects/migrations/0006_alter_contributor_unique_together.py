# Generated by Django 5.1.2 on 2024-11-20 14:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_alter_contributor_unique_together_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='contributor',
            unique_together={('user', 'project')},
        ),
    ]
