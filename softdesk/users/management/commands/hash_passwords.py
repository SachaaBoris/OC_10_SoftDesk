'''
This script is to convert plain passwords to pbkdf2_sha hashed passwords
It makes sure every user has a hashed secure password
Run it with this command :
    py manage.py hash_passwords
'''
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from users.models import User


class Command(BaseCommand):
    help = "Hacher les mots de passes"

    def handle(self, *args, **kwargs):
        # Récupérer tous les utilisateurs avec des mots de passe non hachés
        users = User.objects.exclude(password__startswith='pbkdf2_sha')

        if not users.exists():
            self.stdout.write(self.style.WARNING("Aucun utilisateur vulnérable n'a été trouvé."))
            return

        for user in users:
            # Hacher le mot de passe
            user.password = make_password(user.password)  # Hacher le mot de passe actuel
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Le mot de passe de l’utilisateur {user.username} a été haché.'))

        self.stdout.write(self.style.SUCCESS("Tous les mots de passe non hachés ont été mis à jour avec succès."))
