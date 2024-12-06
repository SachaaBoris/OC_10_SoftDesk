# Dans le shell Django
from projects.models import Comment, Issue

for comment in Comment.objects.all():
    # Extraire l'ID de l'issue à partir de la chaîne actuelle
    issue_id = comment.issue.id
    # Récupérer l'objet Issue correspondant
    issue = Issue.objects.get(id=issue_id)
    # Mettre à jour le commentaire avec la bonne référence
    comment.issue = issue
    comment.save()