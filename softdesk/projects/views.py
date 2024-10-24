from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    SAFE_METHODS,
)
from django.shortcuts import get_object_or_404
from .models import Project, User, Contributor
from .permissions import IsAuthor, IsContributor, IsResponsibleContributor
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    ContributorAutoAssignUserSerializer
)
from .checker import (
    check_and_get_contributor_id,
    check_project_exist_in_db
)


class ProjectViewSet(viewsets.ModelViewSet):
    """A viewset that provides actions for project object."""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a project and set the author as first contributor"""
        project = serializer.save(author_user=self.request.user)
        
        # Add the creator as responsible contributor
        Contributor.objects.create(
            user=self.request.user,
            project=project,
            permission="Responsable",
            role="Auteur"
        )

    def create_project_id_list_connected_user(self):
        """Return project id list of the connected user."""
        project_id_list = []
        connected_user_id = self.request.user.id
        for contributor in Contributor.objects.filter(
            user_id=connected_user_id
        ):
            project_id_list.append(contributor.project_id)

        return project_id_list


class ContributorViewSet(viewsets.ModelViewSet):
    """A viewset that provides actions for contributor object."""

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method not in SAFE_METHODS:
            return [
                permission()
                for permission in [IsResponsibleContributor, IsAuthenticated]
            ]

        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        """Return the class to use for the serializer."""
        if self.action == "update":
            return ContributorAutoAssignUserSerializer
        return super().get_serializer_class()

    def get_object(self):
        """Returns the object the view is displaying."""
        queryset = self.filter_queryset(self.get_queryset())
        kwargs = {}
        user_id = self.kwargs["pk"]
        project_id = self.kwargs["project_pk"]
        contributor_id = check_and_get_contributor_id(project_id, user_id)
        kwargs["pk"] = contributor_id

        obj = get_object_or_404(queryset, **kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        """Get the list of items for this view."""
        project_id = self.kwargs["project_pk"]
        return super().get_queryset().filter(project_id=project_id)

    def perform_create(self, serializer):
        """Create a model instance."""
        project = serializer.save(author_user=self.request.user)

        # Ajoute le créateur comme contributeur
        Contributor.objects.create(
            user=self.request.user,
            project=project,
            permission="Responsable",
            role="Auteur"
        )

        # Vérification des contributeurs
        invalid_users = []
        for username in serializer.validated_data.get('contributors', []):
            try:
                user = User.objects.get(username=username)
                Contributor.objects.create(
                    user=user,
                    project=project,
                    permission="Contributeur",
                    role="Contributeur"
                )
            except User.DoesNotExist:
                invalid_users.append(username)

            if invalid_users:
                return Response(
                    {"warning": f"Les utilisateurs suivants n'existent pas : {', '.join(invalid_users)}"},
                    status=status.HTTP_201_CREATED
                )

    def perform_update(self, serializer):
        """Update a model instance."""
        invalid_users = []

        # Récupération des nouveaux contributeurs à ajouter
        for username in serializer.validated_data.get('contributors', []):
            try:
                user = User.objects.get(username=username)
                serializer.save(user=user)
            except User.DoesNotExist:
                invalid_users.append(username)

        if invalid_users:
            return Response(
                {"warning": f"Les utilisateurs suivants n'existent pas : {', '.join(invalid_users)}"},
                status=status.HTTP_200_OK
            )
        else:
            serializer.save()