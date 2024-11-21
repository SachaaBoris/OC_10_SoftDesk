"""
Custom permissions.
"""
from rest_framework import permissions
from projects.models import Contributor

class IsProjectContributor(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est contributeur du projet.
    """
    def has_object_permission(self, request, view, obj):
        # Obtenir le projet (soit directement, soit via l'issue ou le commentaire)
        if hasattr(obj, 'project'):
            project = obj.project
        else:
            project = obj

        return Contributor.objects.filter(
            user=request.user,
            project=project
        ).exists()

class IsProjectAuthor(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est l'auteur du projet.
    """
    def has_object_permission(self, request, view, obj):
        # Obtenir le projet (soit directement, soit via l'issue ou le commentaire)
        if hasattr(obj, 'project'):
            project = obj.project
        else:
            project = obj
            
        return project.author_user == request.user

class IsProjectContributorOrAuthor(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est soit contributeur soit auteur du projet.
    """
    def has_object_permission(self, request, view, obj):
        # Obtenir le projet (soit directement, soit via l'issue ou le commentaire)
        if hasattr(obj, 'project'):
            project = obj.project
        else:
            project = obj

        # Vérifier si l'utilisateur est l'auteur
        is_author = project.author_user == request.user
        
        # Vérifier si l'utilisateur est contributeur
        is_contributor = Contributor.objects.filter(
            user=request.user,
            project=project
        ).exists()

        return is_author or is_contributor


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est admin ou propriétaire de la ressource.
    """
    def has_object_permission(self, request, view, obj):
        # Admin a tous les droits
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Vérification spécifique selon le type d'objet
        if hasattr(obj, 'author_user'):
            return obj.author_user == request.user
        
        # Pour les utilisateurs, vérifier si c'est le même utilisateur
        if isinstance(obj, User):
            return obj == request.user
        
        return False


class IsAdminOrProjectContributor(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est admin ou contributeur du projet.
    """
    def has_permission(self, request, view):
        # Admin a tous les droits
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Pour les vues sur projet, vérifier si contributeur
        if 'project_pk' in view.kwargs:
            return Contributor.objects.filter(
                user=request.user,
                project_id=view.kwargs['project_pk']
            ).exists()
        
        return False

    def has_object_permission(self, request, view, obj):
        # Admin a tous les droits
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Obtenir le projet (soit directement, soit via l'issue ou le commentaire)
        if hasattr(obj, 'project'):
            project = obj.project
        else:
            project = obj

        return Contributor.objects.filter(
            user=request.user,
            project=project
        ).exists()