"""
Provides checker functions for the "projects" application.
"""
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import User, Project, Contributor


def check_and_get_contributor_id(project_id, user_id):
    """
    Return id contributor according to project and user id or raise exception.
    """
    try:
        project_id = int(project_id)
        user_id = int(user_id)
        return Contributor.objects.get(
            user_id=user_id, project_id=project_id
        ).id
    except Contributor.DoesNotExist:
        raise NotFound("Le contributeur indiqué n'existe pas pour ce projet.")
    except ValueError:
        raise NotFound(
            "Le numéro de contributeur indiqué n'est pas un numéro."
        )


def check_project_exist_in_db(project_id):
    """Raise exception if project object not found in database."""
    try:
        project_id = int(project_id)
        if project_id not in Project.objects.values_list("id", flat=True):
            raise NotFound("Le numéro de projet indiqué n'existe pas.")
    except ValueError:
        raise NotFound("Le numéro de projet indiqué n'est pas un numéro.")


def check_user_email_exist(email):
    if not User.objects.filter(email=email):
        raise serializers.ValidationError(
            "Cet utilisateur n'existe pas."
        )
