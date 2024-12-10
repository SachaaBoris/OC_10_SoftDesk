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

    title = models.CharField(
        max_length=128,
        help_text="Titre du projet."
    )
    description = models.CharField(
        max_length=2048,
        help_text="Description du projet."
    )
    type = models.CharField(
        max_length=9,
        choices=PROJECT_TYPE_CHOICES,
        help_text="Type du projet (back-end, front-end, iOS ou Android)."
    )
    author_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='projects'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de création du projet."
    )

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "user",
            "project",
        )
        ordering = ["user_id"]

    def __str__(self):
        """String for representing the Model object."""
        return f"user: {self.user}, project: {self.project}"


class Issue(models.Model):
    """Issue model."""

    ISSUE_TAG = [
        ("BUG", "BUG"),
        ("AMÉLIORATION", "AMÉLIORATION"),
        ("TÂCHE", "TÂCHE"),
    ]
    ISSUE_PRIORITY = [
        ("FAIBLE", "FAIBLE"),
        ("MOYENNE", "MOYENNE"),
        ("ÉLEVÉE", "ÉLEVÉE"),
    ]
    ISSUE_STATUS = [
        ("À FAIRE", "À FAIRE"),
        ("EN COURS", "EN COURS"),
        ("TERMINÉ", "TERMINÉ"),
    ]

    title = models.CharField(
        max_length=128,
        help_text="Titre du problème."
    )
    description = models.CharField(
        max_length=2048,
        help_text="Description du problème."
    )
    tag = models.CharField(
        max_length=12,
        choices=ISSUE_TAG,
        help_text="Balise du problème (BUG, AMÉLIORATION ou TÂCHE).",
    )
    priority = models.CharField(
        max_length=7,
        choices=ISSUE_PRIORITY,
        help_text="Priorité du problème (FAIBLE, MOYENNE ou ÉLEVÉE).",
    )
    status = models.CharField(
        max_length=8,
        choices=ISSUE_STATUS,
        help_text="Statut du problème (À faire, En cours ou Terminé).",
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    author_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="Issue_author_user",
    )
    assigned_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="Issue_assigned_user",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.id}, {self.title}; project: {self.project}"


class Comment(models.Model):
    """Comment model."""

    description = models.CharField(
        max_length=2048,
        help_text="Corps du commentaire."
    )
    author_user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL
    )
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.id}; issue: {self.issue}"

    @property
    def comment_id(self):
        """Return pk attribut of the object."""
        return self.pk
