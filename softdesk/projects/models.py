from django.db import models
from users.models import User

class Project(models.Model):
    """Project model."""

    PROJECT_TYPE_CHOICES = [
        ("Back-End", "Back-End"),
        ("Front-End", "Front-End"),
        ("iOs", "iOs"),
        ("Android", "Android"),
    ]

    title = models.CharField(max_length=128, help_text="Titre du projet.")
    description = models.CharField(
        max_length=2048, help_text="Description du projet."
    )
    type = models.CharField(
        max_length=9,
        choices=PROJECT_TYPE_CHOICES,
        help_text="Type du projet (back-end, front-end, iOS ou Android).",
    )
    author_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date de création du projet.")

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.title}"

    @property
    def project_id(self):
        """Return pk attribut of the object."""
        return self.pk


class Contributor(models.Model):
    """Contributor model."""

    PERMISSION_CHOICES = [
        ("Responsable", "Responsable"),
        ("Contributeur", "Contributeur"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(
        max_length=12,
        choices=PERMISSION_CHOICES,
    )
    role = models.CharField(
        max_length=128, blank=True, help_text="Rôle du contributeur."
    )

    class Meta:
        unique_together = (
            "user",
            "project",
        )
        ordering = ["user_id"]

    def __str__(self):
        """String for representing the Model object."""
        return f"user: {self.user}, project: {self.project}"
