from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from .models import Project, Contributor
from .forms import ProjectAdminForm


class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model"""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("username", "age")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "age",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("email", "username", "age", "is_staff")
    search_fields = ("email", "username", "age")
    ordering = ("username",)


class ContributorInline(admin.TabularInline):
    """Inline admin descriptor for Contributor model."""
    model = Contributor
    extra = 1  # Number of extra empty forms in the admin


class ContributorAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'permission']  # Liste des champs visibles

    def get_readonly_fields(self, request, obj=None):
        """Rendre le champ project en lecture seule pour un contributeur existant."""
        if obj:  # Si l'objet existe (pour l'édition, pas pour la création)
            return ['project']  # Rendre le champ `project` en lecture seule
        return []


class ProjectAdmin(admin.ModelAdmin):
    """Admin view for Project."""

    # Affichage des champs dans la vue d'administration
    list_display = ("title", "author_user", "type", "created_at", "get_contributors")
    fields = ("title", "description", "type", "author_user", "created_at")

    readonly_fields = ("created_at", "author_user")
    
    # Ajouter les contributeurs en inline
    inlines = [ContributorInline]

    def get_contributors(self, obj):
        """Returns a comma-separated list of contributors for a project."""
        return ", ".join([contrib.user.username for contrib in obj.contributor_set.all()])
        #contributors = Contributor.objects.filter(project=obj)
        #return ", ".join([contrib.user.username for contrib in contributors])

    get_contributors.short_description = 'Contributors'


# Register your models here.
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Project, ProjectAdmin)