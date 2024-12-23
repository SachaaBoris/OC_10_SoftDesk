# Generated by Django 5.1.2 on 2024-10-23 11:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Titre du projet.', max_length=128)),
                ('description', models.CharField(help_text='Description du projet.', max_length=2048)),
                ('type', models.CharField(choices=[('Back-End', 'Back-End'), ('Front-End', 'Front-End'), ('iOs', 'iOs'), ('Android', 'Android')], help_text='Type du projet (back-end, front-end, iOS ou Android).', max_length=9)),
                ('author_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.CharField(choices=[('Responsable', 'Responsable'), ('Contributeur', 'Contributeur')], max_length=12)),
                ('role', models.CharField(blank=True, help_text='Rôle du contributeur.', max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'ordering': ['user_id'],
                'unique_together': {('user', 'project')},
            },
        ),
    ]
