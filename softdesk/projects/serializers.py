"""
Provides application serializers
"""
from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment
from django.shortcuts import get_object_or_404


class ContributorSerializer(serializers.ModelSerializer):
    # Définir un champ 'contributors' pour accepter une liste de usernames (pour l'écriture)
    contributors = serializers.ListField(child=serializers.CharField(), write_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'username', 'email', 'project', 'contributors']
        read_only_fields = ['project', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view_action') == 'list':
            # Limiter les champs pour la liste
            self.fields.pop('project', None)
            self.fields.pop('user', None)
            self.fields.pop('username')
            self.fields.pop('email')
        else:
            self.fields.pop('project', None)
            self.fields.pop('id', None)
            self.fields.pop('user', None)

    def to_representation(self, instance):
        # Vérifier que l'instance est un objet du modèle Contributor
        if not hasattr(instance, 'user'):
            # Si ce n'est pas une instance Contributor, retourner la représentation de base
            return super().to_representation(instance)

        # Obtient la représentation par défaut
        representation = super().to_representation(instance)

        # Vérifie si l'utilisateur peut être contacté
        if not instance.user.can_be_contacted:
            representation.pop('email', None)

        return representation

    def create(self, validated_data):
        contributors_usernames = validated_data.pop('contributors', [])
        # Récupérer le projet depuis l'URL de la requête
        project_pk = self.context['view'].kwargs['project_pk']
        project = Project.objects.get(pk=project_pk)

        created_contributors = []
        error_messages = []

        for username in contributors_usernames:
            try:
                # Vérifier si l'utilisateur avec ce username existe
                user = User.objects.get(username=username)

                # Vérifier si l'utilisateur est déjà un contributeur pour ce projet
                if not Contributor.objects.filter(user=user, project=project).exists():
                    # S'il n'est pas encore un contributeur, on l'ajoute au projet
                    contributor = Contributor.objects.create(user=user, project=project)
                    created_contributors.append(contributor)
                else:
                    # Si l'utilisateur est déjà contributeur, ajouter un message d'erreur
                    error_messages.append(f"L'utilisateur '{username}' est déjà contributeur du projet.")
            except User.DoesNotExist:
                # Si l'utilisateur n'existe pas, ajouter un message d'erreur
                error_messages.append(f"L'utilisateur '{username}' n'existe pas.")
            except Exception as e:
                # En cas d'autre erreur (ex : erreur de base de données), ajouter un message d'erreur
                error_messages.append(f"Erreur lors de l'ajout de l'utilisateur '{username}' : {str(e)}")

        # Si des erreurs sont présentes et aucun contributeur n'a été créé, lever une exception
        if error_messages and not created_contributors:
            raise serializers.ValidationError({"errors": error_messages})

        # Retourner la liste des contributeurs crées ou rien
        return created_contributors or None


class ContributorIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id']  # Seulement l'ID du contributeur


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'description',
            'author_user',
            'issue',
            'created_at'
        ]
        read_only_fields = ['author_user', 'issue', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view_action') == 'list':
            self.fields.pop('issue', None)
            self.fields.pop('created_at', None)

    def validate(self, data):
        if self.instance:  # En mise à jour
            issue = self.instance.issue
        else:  # En création
            view = self.context['view']
            project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
            issue = get_object_or_404(
                Issue,
                pk=view.kwargs['issue_pk'],
                project=project
            )

        project_pk = self.context['view'].kwargs['project_pk']

        if issue.project.id != int(project_pk):
            raise serializers.ValidationError("L'issue ne correspond pas au projet.")
        return data


class IssueSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(default="TÂCHE")
    priority = serializers.CharField(default="MOYENNE")
    status = serializers.CharField(default="En cours")
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'description',
            'tag',
            'priority',
            'status',
            'assigned_user',
            'project',
            'author_user',
            'created_at',
            'comments'
        ]
        read_only_fields = ['project', 'author_user', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view_action') == 'list':
            # Limiter les champs pour la liste
            self.fields.pop('description', None)
            self.fields.pop('tag', None)
            self.fields.pop('priority', None)
            self.fields.pop('assigned_user', None)
            self.fields.pop('project', None)
            self.fields.pop('created_at', None)
            self.fields.pop('comments', None)
        else:
            # Obtenir l'instance de l'objet si disponible
            instance = self.instance if hasattr(self, 'instance') else None
            if instance:
                # Supprimer les champs si vides ou non attribués
                if not getattr(instance, 'assigned_user', None):  # Vérifie si assigned_user est défini
                    self.fields.pop('assigned_user', None)
                if instance.comment_set.count() == 0:
                    self.fields.pop('comments', None)

    def get_comments(self, obj):
        comments = Comment.objects.filter(issue=obj)
        # Récupérer uniquement les IDs des commentaires liés à l'issue actuelle
        return list(comments.values_list('id', flat=True))
        # Récupérer tous les commentaires liés à l'issue actuelle
        # return CommentSerializer(comments, many=True).data


class ProjectSerializer(serializers.ModelSerializer):
    contributors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )
    project_contributors = ContributorIdSerializer(
        source='contributor_set',
        many=True,
        read_only=True
    )
    issues = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author_user',
            'created_at',
            'contributors',
            'project_contributors',
            'issues'
        ]
        read_only_fields = ['author_user', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('view_action') == 'list':
            self.fields.pop('description', None)
            self.fields.pop('created_at', None)
            self.fields.pop('contributors', None)
            self.fields.pop('project_contributors', None)
            self.fields.pop('issues', None)
        else:
            instance = self.instance if hasattr(self, 'instance') else None
            if instance:
                if instance.contributor_set.count() == 0:
                    self.fields.pop('project_contributors', None)
                if instance.issue_set.count() == 0:
                    self.fields.pop('issues', None)

    def get_issues(self, obj):
        return list(Issue.objects.filter(project=obj).values_list('id', flat=True))

    def _manage_contributors(self, project, usernames, author_user):
        """
        Méthode pour gérer les contributeurs d'un projet
        """
        # Créer/Vérifier le contributeur auteur
        try:
            Contributor.objects.get_or_create(
                user=author_user,
                project=project
            )
        except Exception as e:
            raise serializers.ValidationError(
                f"Erreur lors de la gestion du contributeur auteur : {str(e)}"
            )

        # Gérer les autres contributeurs
        current_contributors = set(project.contributor_set.values_list('user__username', flat=True))
        new_contributors = set(usernames)

        # Ajouter les nouveaux contributeurs
        for username in new_contributors - current_contributors:
            try:
                user = User.objects.get(username=username)
                if user != author_user:
                    Contributor.objects.get_or_create(
                        user=user,
                        project=project
                    )
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    f"Utilisateur non trouvé : {username}"
                )
            except Exception as e:
                raise serializers.ValidationError(
                    f"Erreur lors de l'ajout du contributeur {username} : {str(e)}"
                )

        # Supprimer les contributeurs retirés (sauf l'auteur)
        contributors_to_remove = current_contributors - new_contributors - {author_user.username}
        if contributors_to_remove:
            Contributor.objects.filter(
                project=project,
                user__username__in=contributors_to_remove
            ).delete()

    def create(self, validated_data):
        contributors = validated_data.pop('contributors', [])
        try:
            project = Project.objects.create(**validated_data)
            self._manage_contributors(project, contributors, validated_data['author_user'])
            return project
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la création du projet : {str(e)}")

    def update(self, instance, validated_data):
        contributors = validated_data.pop('contributors', [])
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            self._manage_contributors(instance, contributors, instance.author_user)
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Erreur lors de la mise à jour du projet : {str(e)}")
