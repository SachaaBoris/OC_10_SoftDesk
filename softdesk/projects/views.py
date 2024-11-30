from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer
)
from .permissions import (
    IsAdminOrOwner, 
    IsAdminOrProjectContributor, 
    IsProjectAuthor
)
from config.pagination import (
    UserPagination,
    ProjectPagination,
    IssuePagination,
    CommentPagination
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Ajoute l'action (list ou retrieve) dans le contexte
        context['view_action'] = self.action
        return context
    
    def get_permission_classes(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list':
            return [IsAuthenticated]  # Pour la liste, seulement authentifié suffit
        return [IsAuthenticated, IsAdminOrProjectContributor]  # Pour les autres actions

    def get_queryset(self):
        user = self.request.user
        # Si admin, tous les projets
        if user.is_staff or user.is_superuser:
            return Project.objects.all()
        # Pour les utilisateurs normaux, uniquement les projets où ils sont contributeurs
        return Project.objects.filter(contributor__user=user).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectContributor]
    pagination_class = UserPagination

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        # Si admin, tous les contributeurs, sinon vérifier
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Contributor.objects.filter(project_id=project_pk)

        # Vérifier si l'utilisateur est contributeur du projet
        return Contributor.objects.filter(
            project_id=project_pk,
            project__contributor__user=self.request.user
        )

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(project=project)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectContributor]
    pagination_class = IssuePagination

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        # Si admin, toutes les issues, sinon vérifier
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Issue.objects.filter(project_id=project_pk)

        return Issue.objects.filter(
            project_id=project_pk,
            project__contributor__user=self.request.user
        )

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(
            project=project,
            author_user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        # Seul l'auteur de l'issue ou l'admin peut modifier
        instance = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser or instance.author_user == request.user):
            return Response(
                {"detail": "Vous n'êtes pas autorisé à modifier cette issue."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrProjectContributor]
    pagination_class = CommentPagination

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']

        # Si admin, tous les commentaires, sinon vérifier
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Comment.objects.filter(
                issue__project_id=project_pk, 
                issue_id=issue_pk
            )

        return Comment.objects.filter(
            issue__project_id=project_pk,
            issue_id=issue_pk,
            issue__project__contributor__user=self.request.user
        )

    def perform_create(self, serializer):
        issue = get_object_or_404(
            Issue, 
            pk=self.kwargs['issue_pk'], 
            project_id=self.kwargs['project_pk']
        )
        serializer.save(
            issue=issue,
            author_user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        # Seul l'auteur du commentaire ou l'admin peut modifier
        instance = self.get_object()
        if not (request.user.is_staff or request.user.is_superuser or instance.author_user == request.user):
            return Response(
                {"detail": "Vous n'êtes pas autorisé à modifier ce commentaire."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
