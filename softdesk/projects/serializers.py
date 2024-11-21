"""
Provides application serializers
"""
from rest_framework import serializers
#from django.contrib.auth.password_validation import validate_password
from .models import User, Project, Contributor, Issue, Comment


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'permission', 'role']
        read_only_fields = ['project']


class ProjectListSerializer(serializers.ModelSerializer):
    """Project object serializer."""
    contributors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )
    contributors_details = ContributorSerializer(source='contributor_set', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user', 'contributors', 'contributors_details']
        read_only_fields = ['author_user']

    def create(self, validated_data):
        try:
            # Extraire et supprimer les contributeurs des données validées
            contributors_usernames = validated_data.pop('contributors', [])
            
            # Créer le projet
            project = Project.objects.create(**validated_data)
            
            # Créer le contributeur pour l'auteur dans une transaction
            try:
                Contributor.objects.create(
                    user=validated_data['author_user'],
                    project=project,
                    permission="Responsable",
                    role="Auteur"
                )
            except Exception as e:
                print(f"Erreur lors de la création du contributeur auteur: {e}")
                
            # Ajouter les autres contributeurs
            for username in contributors_usernames:
                try:
                    user = User.objects.get(username=username)
                    if user != validated_data['author_user']:
                        try:
                            Contributor.objects.create(
                                user=user,
                                project=project,
                                permission="Contributeur",
                                role="Contributeur"
                            )
                        except Exception as e:
                            print(f"Erreur lors de la création du contributeur {username}: {e}")
                except User.DoesNotExist:
                    print(f"Utilisateur non trouvé: {username}")
            
            return project
            
        except Exception as e:
            print(f"Erreur lors de la création du projet: {e}")
            raise serializers.ValidationError(f"Erreur lors de la création du projet: {str(e)}")


class ProjectDetailSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(source='contributor_set', many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user', 'created_at', 'contributors']
        read_only_fields = ['author_user', 'created_at']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'assigned_user',
                 'project', 'author_user', 'created_time']
        read_only_fields = ['project', 'author_user', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author_user', 'issue', 'created_time']
        read_only_fields = ['author_user', 'issue', 'created_time']
