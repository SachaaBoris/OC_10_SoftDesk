from projects.models import Contributor

# Trouver les contributeurs avec le rôle incorrect
incorrect_contributors = Contributor.objects.filter(role="Auteur du projet")

# Corriger les rôles pour ces contributeurs
for contributor in incorrect_contributors:
    contributor.role = "Auteur"  # ou "Auteur", selon ce que tu souhaites
    contributor.save()

print(f"{incorrect_contributors.count()} contributeurs corrigés.")