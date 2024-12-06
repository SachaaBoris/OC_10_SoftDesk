from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    ContributorIdSerializer,
    IssueSerializer,
    CommentSerializer
)
from .permissions import (
    IsAdmin, 
    IsAuthor,
    IsAuthorOrIsAdmin,
    IsProjectContributor,
    IsProjectContributorOrIsAdmin
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
    
    def get_permissions(self):
        if self.action in ['list', 'create']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve']:
            permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        else:  # Permission par defaut
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        # Si admin, tous les projets
        if user.is_superuser:
            return Project.objects.all()
        # Autrement, ne lister que les projets où ils sont contributeurs
        return Project.objects.filter(contributor__user=user).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "Vous n'êtes contributeur d'aucun projet pour l'instant."})
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        project = serializer.save(author_user=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    queryset = Contributor.objects.all()
    pagination_class = UserPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
        elif self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        else:  # Permission par defaut
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Ajoute l'action (list ou retrieve) dans le contexte
        context['view_action'] = self.action
        return context

    def get_queryset(self):
        """
        Retourne les contributeurs d'un projet spécifique.
        Seuls les contributeurs du projet ou l'administrateur peuvent voir cette liste.
        """
        project_pk = self.kwargs['project_pk']

        if self.request.user.is_superuser:
            return Contributor.objects.filter(project_id=project_pk)

        is_contributor = Contributor.objects.filter(
            project_id=project_pk,
            user=self.request.user
        ).exists()

        if is_contributor:
            return Contributor.objects.filter(project_id=project_pk)

        # Si l'utilisateur n'est ni contributeur ni admin, aucune permission
        raise PermissionDenied("Vous devez être contributeur du projet pour accéder à ces informations.")

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        
        # Vérifie si l'utilisateur est l'auteur du projet ou un administrateur
        if not (self.request.user == project.author_user or self.request.user.is_superuser):
            raise PermissionDenied("Vous devez être l'auteur du projet pour ajouter des contributeurs.")
        
        # Sauvegarde le contributeur
        serializer.save(project=project)
        
        # Liste des utilisateurs à ajouter
        contributors_usernames = request.data.get('contributors', [])

        messages = []
        
        for username in contributors_usernames:
            try:
                user = User.objects.get(username=username)
                if user != serializer.validated_data['author_user']:
                    Contributor.objects.create(
                        user=user,
                        project=serializer.validated_data['project']
                    )
                    messages.append(f"Le contributeur '{username}' a bien été ajouté au projet {serializer.validated_data['project'].id}.")
                else:
                    messages.append(f"Le contributeur '{username}' est déjà l'auteur du projet.")
            except User.DoesNotExist:
                messages.append(f"Utilisateur '{username}' non trouvé.")
            except Exception as e:
                messages.append(f"Erreur lors de l'ajout du contributeur '{username}': {str(e)}")
        
        # Retourne les messages et les données
        return Response(
            {
                "message": "Contributeurs ajoutés avec succès.",
                "details": messages,
            },
            status=status.HTTP_201_CREATED
        )
    
    def destroy(self, request, *args, **kwargs):
        # Vérifiez si l'utilisateur actuel est l'auteur du projet
        contributor = self.get_object()
        if contributor.project.author_user != request.user:
            raise PermissionDenied("Vous devez être l'auteur du projet pour supprimer ce contributeur.")
        
        # Si l'utilisateur est l'auteur, effectuez la suppression
        return super().destroy(request, *args, **kwargs)


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
    pagination_class = IssuePagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Ajoute l'action (list ou retrieve) dans le contexte
        context['view_action'] = self.action
        return context
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        else:  # Permission par defaut
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        # Si admin, toutes les issues, sinon vérifier
        if self.request.user.is_superuser:
            return Issue.objects.filter(project_id=project_pk)

        return Issue.objects.filter(
            project_id=project_pk,
            project__contributor__user=self.request.user
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "Il n'y a pas d'issue ici."},
                status=200
            )
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        serializer.save(
            project=project,
            author_user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        # Seul l'auteur de l'issue ou l'admin peut modifier
        instance = self.get_object()
        if not (request.request.user.is_superuser or instance.author_user == request.user):
            return Response(
                {"detail": "Vous n'êtes pas autorisé à modifier cette issue."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
    pagination_class = CommentPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Ajoute l'action (list ou retrieve) dans le contexte
        context['view_action'] = self.action
        return context

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
        elif self.action in ['destroy']:
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        else:  # Permission par defaut
            permission_classes = [IsAuthenticated, IsAuthorOrIsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):    
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])
        base_queryset = Comment.objects.select_related('issue', 'issue__project')

        if self.request.user.is_superuser:
            print("Utilisateur est superuser")
            queryset = base_queryset.filter(
                issue=issue,
                issue__project=project
            )
        else:
            print("Utilisateur est contributeur")
            queryset = base_queryset.filter(
                issue=issue,
                issue__project=project,
                issue__project__contributor__user=self.request.user
            )

        return queryset

    def get_object(self): 
        queryset = self.get_queryset()
        comment_pk = self.kwargs.get('pk')

        try:
            obj = get_object_or_404(queryset, pk=comment_pk)
        except Http404:
            raise Http404({"message": "Ce commentaire n'existe pas."})

        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"message": "Il n'y a pas de commentaire ici."},
                status=200
            )
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        issue = get_object_or_404(
            Issue, 
            pk=self.kwargs['issue_pk'], 
            project=project
        )
        serializer.save(
            issue=issue,
            author_user=self.request.user
        )

    def update(self, request, *args, **kwargs):
        # Seul l'auteur du commentaire ou l'admin peut modifier
        instance = self.get_object()
        if not (request.request.user.is_superuser or instance.author_user == request.user):
            return Response(
                {"detail": "Vous n'êtes pas autorisé à modifier ce commentaire."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


#class CommentViewSet(viewsets.ModelViewSet):
#    serializer_class = CommentSerializer
#    permission_classes = [IsAuthenticated, IsProjectContributorOrIsAdmin]
#    pagination_class = CommentPagination
#
#    def get_serializer_context(self):
#        context = super().get_serializer_context()
#        context['view_action'] = self.action
#        return context
#
#    def get_object(self):
#        import traceback
#        print("=== Début get_object ===")
#        
#        # Afficher la stack trace
#        print("Stack trace:")
#        traceback.print_stack()
#        
#        try:
#            project = Project.objects.get(pk=self.kwargs['project_pk'])
#            print(f"Type de project: {type(project)}")
#            print(f"Project ID: {project.id}")
#            
#            issue = Issue.objects.get(pk=self.kwargs['issue_pk'], project=project)
#            print(f"Type de issue: {type(issue)}")
#            print(f"Issue ID: {issue.id}")
#            
#            comment = Comment.objects.select_related(
#                'issue', 
#                'issue__project'
#            ).get(
#                pk=self.kwargs['pk'],
#                issue=issue
#            )
#            print(f"Type de comment: {type(comment)}")
#            print(f"Comment ID: {comment.id}")
#            
#            self.check_object_permissions(self.request, comment)
#            return comment
#            
#        except Exception as e:
#            print(f"Exception dans get_object: {str(e)}")
#            print("Stack trace de l'erreur:")
#            traceback.print_exc()
#            raise
#
#    def get_queryset(self):
#        return Comment.objects.none()  # Temporairement désactivé pour debug