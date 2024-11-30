# Generated by Django 5.1.2 on 2024-11-18 09:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Titre du problème.', max_length=128)),
                ('desc', models.CharField(help_text='Description du problème.', max_length=2048)),
                ('tag', models.CharField(choices=[('BUG', 'BUG'), ('AMÉLIORATION', 'AMÉLIORATION'), ('TÂCHE', 'TÂCHE')], help_text='Balise du problème (BUG, AMÉLIORATION ou TÂCHE).', max_length=12)),
                ('priority', models.CharField(choices=[('FAIBLE', 'FAIBLE'), ('MOYENNE', 'MOYENNE'), ('ÉLEVÉE', 'ÉLEVÉE')], help_text='Priorité du problème (FAIBLE, MOYENNE ou ÉLEVÉE).', max_length=7)),
                ('status', models.CharField(choices=[('À FAIRE', 'À FAIRE'), ('EN COURS', 'EN COURS'), ('TERMINÉ', 'TERMINÉ')], help_text='Statut du problème (À faire, En cours ou Terminé).', max_length=8)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assigned_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Issue_assigned_user', to=settings.AUTH_USER_MODEL)),
                ('author_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Issue_author_user', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='corps du commentaire.', max_length=2048)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.issue')),
            ],
            options={
                'ordering': ['-created_time'],
            },
        ),
    ]