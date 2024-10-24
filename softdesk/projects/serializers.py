"""
Provides serializers for objects of "projects" application.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Project, Contributor
from .checker import check_user_email_exist, check_and_get_contributor_id


class ProjectSerializer(serializers.ModelSerializer):
    """Project object serializer."""
    contributors = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        write_only=True
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author_user', 'contributors']
        read_only_fields = ['author_user']

    def create(self, validated_data):
        # Extract contributors from validated_data
        contributors_usernames = validated_data.pop('contributors', [])
        
        # Create project
        project = Project.objects.create(**validated_data)
        
        # Add contributors
        missing_users = []
        for username in contributors_usernames:
            try:
                user = User.objects.get(username=username)
                Contributor.objects.create(
                    user=user,
                    project=project,
                    permission="Contributeur",
                    role="Contributeur"
                )
            except User.DoesNotExist:
                missing_users.append(username)
        
        if missing_users:
            # Note: You might want to handle this warning differently
            print(f"Warning: Users not found: {', '.join(missing_users)}")
            
        return project


class ContributorSerializer(serializers.ModelSerializer):
    """Contributor object serializer."""

    project_id = serializers.ReadOnlyField()
    user_id = serializers.ReadOnlyField()
    user = serializers.EmailField(write_only=True)

    def validate_user(self, value):
        """Return user object"""
        check_user_email_exist(value)
        project_id = self.context["request"].parser_context["kwargs"][
            "project_pk"
        ]
        user = User.objects.get(email=value)
        if self.context["request"].method == "POST":
            if Contributor.objects.filter(
                project_id=project_id, user_id=user.id
            ):
                """Or raise validation error."""
                raise serializers.ValidationError(
                    "Cet utilisateur est déjà contributeur du projet."
                )

        return user

    class Meta:
        model = Contributor
        fields = (
            "user_id",
            "user",
            "project_id",
            "permission",
            "role",
        )


class ContributorAutoAssignUserSerializer(serializers.ModelSerializer):
    """Contributor with hidden user field object serializer."""

    user = serializers.HiddenField(default="")

    class Meta:
        model = Contributor
        fields = (
            "user_id",
            "user",
            "project_id",
            "permission",
            "role",
        )
