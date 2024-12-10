"""
URL configuration
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from users.views import (
    UserViewSet,
)
from projects.views import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
)

# Router principal
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'projects', ProjectViewSet, basename='projects')

# Router imbriqué pour les contributeurs
contributors_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)
contributors_router.register(
    r'contributors',
    ContributorViewSet,
    basename='project-contributors'
)

# Router imbriqué pour les issues
issues_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='project'
)
issues_router.register(
    r'issues',
    IssueViewSet,
    basename='project-issues'
)

# Router imbriqué pour les commentaires
comments_router = routers.NestedDefaultRouter(
    issues_router,
    r'issues',
    lookup='issue'
)
comments_router.register(
    r'comments',
    CommentViewSet,
    basename='issue-comments'
)

# Combine URL patterns
urlpatterns = [
    # Admin
    path('softdesk_api/admin/', admin.site.urls),

    # Authentication endpoints
    path('softdesk_api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('softdesk_api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API endpoints
    path('softdesk_api/', include([
        path('', include(router.urls)),
        path('', include(contributors_router.urls)),
        path('', include(issues_router.urls)),
        path('', include(comments_router.urls)),
    ])),
]


''' API Endpoints :
•
••• Authentication
• POST   /softdesk_api/login/                                                           • Obtenir un token JWT
• POST   /softdesk_api/login/refresh/                                                   • Rafraîchir un token JWT
•
••• Users
• GET    /softdesk_api/users/                                                           • Liste des utilisateurs (admin)
• POST   /softdesk_api/users/                                                           • Créer un utilisateur
• GET    /softdesk_api/users/{user_id}/                                                 • Détails d'un utilisateur
• PUT    /softdesk_api/users/{user_id}/                                                 • Modifier un utilisateur
• DELETE /softdesk_api/users/{user_id}/                                                 • Supprimer un utilisateur
•
••• Projects
• GET    /softdesk_api/projects/                                                        • Liste des projets
• POST   /softdesk_api/projects/                                                        • Créer un projet
• GET    /softdesk_api/projects/{project_id}/                                           • Détails d'un projet
• PUT    /softdesk_api/projects/{project_id}/                                           • Modifier un projet
• DELETE /softdesk_api/projects/{project_id}/                                           • Supprimer un projet
•
••• Contributors
• GET    /softdesk_api/projects/{project_id}/contributors/                              • Liste des contributeurs
• POST   /softdesk_api/projects/{project_id}/contributors/                              • Ajouter un contributeur
• GET    /softdesk_api/projects/{project_id}/contributors/{contributor_id}/             • Détails d'un contributeur
• DELETE /softdesk_api/projects/{project_id}/contributors/{contributor_id}/             • Supprimer un contributeur
•
••• Issues
• GET    /softdesk_api/projects/{project_id}/issues/                                    • Liste des issues
• POST   /softdesk_api/projects/{project_id}/issues/                                    • Créer une issue
• GET    /softdesk_api/projects/{project_id}/issues/{issue_id}/                         • Détails d'une issue
• PUT    /softdesk_api/projects/{project_id}/issues/{issue_id}/                         • Modifier une issue
• DELETE /softdesk_api/projects/{project_id}/issues/{issue_id}/                         • Supprimer une issue
•
••• Comments
• GET    /softdesk_api/projects/{project_id}/issues/{issue_id}/comments/                • Liste des commentaires
• POST   /softdesk_api/projects/{project_id}/issues/{issue_id}/comments/                • Créer un commentaire
• GET    /softdesk_api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/   • Détails d'un commentaire
• PUT    /softdesk_api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/   • Modifier un commentaire
• DELETE /softdesk_api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/   • Supprimer un commentaire


••• API Permissions :
•
••• Users
• GET     • authenticated user > liste tous les users
• POST    • not authenticated + formulaire valide > crée un user
• GET     • user_id == authenticated user ou admin > donne les infos d'un user
• PUT     • user_id == authenticated user ou admin > update les infos d'un user
• DELETE  • user_id == authenticated user ou admin > delete un user
•
••• Projets
• GET     • authenticated contrib ou admin > liste tous les projets pour l'admin, contributed projects pour les users
• POST    • authenticated user > crée un projet et des contributeurs
• GET     • authenticated contrib ou admin
• PUT     • authenticated project_author ou admin
• DELETE  • authenticated project_author ou admin
•
••• Contributeurs
• GET     • authenticated contributor ou admin > liste les contributeurs d'un projet
• POST    • authenticated project_author ou admin > ajoute un ou plusieurs contributeurs
• GET     • authenticated contributor ou admin > get contributor info si user "can_be_contacted" est true
• DELETE  • authenticated project_author ou admin > delete un ou plusieurs contributeurs
•
••• Issues
• GET     • authenticated contributor ou admin > liste les issues d'un projet
• POST    • authenticated contributor ou admin > crée une issue associé à un projet
• GET     • authenticated contributor ou admin > donne les infos d'une issue
• PUT     • authenticated issue_author ou admin > update les infos d'une issue
• DELETE  • authenticated issue_author ou admin > delete une issue
•
••• Commentaires
• GET     • authenticated contributor ou admin > liste les issues d'un projet
• POST    • authenticated contributor ou admin > crée un comment
• GET     • authenticated contributor ou admin > liste les comments d'une issue
• PUT     • authenticated comment_author ou admin > update le comment
• DELETE  • authenticated comment_author ou admin > delete le comment
'''
