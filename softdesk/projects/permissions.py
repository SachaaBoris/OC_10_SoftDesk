"""
Custom permissions.
"""
from rest_framework.permissions import BasePermission
from rest_framework import permissions
from projects.models import Contributor


class IsAdmin(permissions.BasePermission):
    """
    Permission permettant uniquement aux super administrateurs d'accéder à la ressource.
    """
    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsAuthor(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est l'auteur de la ressource.
    """
    def has_object_permission(self, request, view, obj):
        # Vérifie si l'objet possède un champ 'author_user' et compare avec l'utilisateur authentifié
        if hasattr(obj, 'author_user'):
            return obj.author_user == request.user

        return False


class IsProjectContributor(permissions.BasePermission):
    """
    Permission vérifiant si l'utilisateur est contributeur d'un projet.
    """
    message = "Vous devez être contributeur pour accéder à ce projet."

    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs:
            project_id = view.kwargs['project_pk']
        elif 'pk' in view.kwargs:
            project_id = view.kwargs['pk']
        else:
            return False

        return Contributor.objects.filter(
            user=request.user,
            project_id=project_id
        ).exists()

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project
        else:
            project = obj

        return Contributor.objects.filter(
            user=request.user,
            project=project
        ).exists()


class IsProjectContributorOrIsAdmin(BasePermission):
    """
    Permission vérifiant si l'utilisateur est soit contributeur d'un projet soit superuser.
    """
    message = "Vous devez être contributeur ou administrateur pour accéder à cette ressource."

    def has_permission(self, request, view):
        return (
            request.user
            and (
                IsProjectContributor().has_permission(request, view)
                or IsAdmin().has_permission(request, view)
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            IsProjectContributor().has_object_permission(request, view, obj)
            or IsAdmin().has_object_permission(request, view, obj)
        )


class IsAuthorOrIsAdmin(BasePermission):
    """
    Permission vérifiant si l'utilisateur est soit auteur d'un projet soit superuser.
    """
    message = "Vous devez être l'auteur ou administrateur pour effectuer cette action."

    def has_permission(self, request, view):
        return request.user and IsAdmin().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return (
            IsAuthor().has_object_permission(request, view, obj)
            or IsAdmin().has_object_permission(request, view, obj)
        )
