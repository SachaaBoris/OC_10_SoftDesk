"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import SimpleRouter
from users.views import SignUp, UserViewSet, MyInfo
from projects.views import ProjectViewSet, ContributorViewSet
from rest_framework_nested import routers

# Router for users
user_router = SimpleRouter()
user_router.register(r"accounts", UserViewSet, basename="user")

# Router for projects
project_router = SimpleRouter()
project_router.register(r"projects", ProjectViewSet, basename="projects")

# Nested router for project contributors
projects_router = routers.NestedSimpleRouter(project_router, r"projects", lookup="project")
projects_router.register(r"users", ContributorViewSet, basename="project-users")

# Combine all URL patterns
urlpatterns = user_router.urls + project_router.urls + projects_router.urls

urlpatterns += [
    path("softdesk_api/admin/", admin.site.urls),
    path(
        "softdesk_api/login/",
        jwt_views.TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "softdesk_api/login/refresh/",
        jwt_views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("softdesk_api/signup/", SignUp.as_view()),
    path("softdesk_api/myinfo/", MyInfo.as_view()),
    path("softdesk_api/projects/create/", ProjectViewSet.as_view({'post': 'create'}), name='project-create'),
]

# URLs List :
# ^accounts/$ [name='user-list']
# ^accounts/(?P<pk>[^/.]+)/$ [name='user-detail']
# ^projects/$ [name='projects-list']
# ^projects/(?P<pk>[^/.]+)/$ [name='projects-detail']
# ^projects/(?P<project_pk>[^/.]+)/users/$ [name='project-users-list']
# ^projects/(?P<project_pk>[^/.]+)/users/(?P<pk>[^/.]+)/$ [name='project-users-detail']
# sofdesk_api/admin/
# sofdesk_api/login/ [name='token_obtain_pair']
# sofdesk_api/login/refresh/ [name='token_refresh']
# sofdesk_api/signup/
# sofdesk_api/myinfo/