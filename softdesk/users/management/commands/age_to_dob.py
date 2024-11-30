from datetime import date, timedelta
import random
from django.core.management.base import BaseCommand
from users.models import User  # Remplacez 'users.models' par le chemin correct vers votre modèle User


class Command(BaseCommand):
    help = "Convertit le champ 'age' en 'dob' dans la base de données."

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            if hasattr(user, 'age') and user.age:  # Vérifie si l'attribut existe et est valide
                # Calculer l'année de naissance en fonction de l'âge actuel
                year_of_birth = date.today().year - user.age
                
                # Générer une date aléatoire pour l'anniversaire
                random_day = random.randint(1, 365)
                dob = date(year_of_birth, 1, 1) + timedelta(days=random_day - 1)
                
                # Mettre à jour la date de naissance
                user.dob = dob
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Utilisateur {user.id} mis à jour avec DOB: {dob}"))
            else:
                self.stdout.write(self.style.WARNING(f"Utilisateur {user.id} : champ 'age' manquant ou invalide."))