from django import forms
from .models import Project, Contributor
from .models import User  # Importez le modèle User personnalisé

class ProjectAdminForm(forms.ModelForm):
    user_to_add = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        help_text="Sélectionnez un utilisateur à ajouter comme contributeur."
    )

    class Meta:
        model = Project
        fields = ['title', 'type', 'description']

    def save(self, commit=True):
        # Sauvegarde du projet d'abord (uniquement si commit=True)
        project = super().save(commit=commit)
        
        # Après que le formulaire soit entièrement validé et posté, ajout des contributeurs
        user = self.cleaned_data.get('user_to_add')
        if user:
            Contributor.objects.create(
                user=user,
                project=project,
                permission="Contributeur",  # Vous pouvez ajuster ce rôle
                role="Contributeur"
            )

        return project