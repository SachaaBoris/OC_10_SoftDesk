from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 10  # Utilisateurs par page
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProjectPagination(PageNumberPagination):
    page_size = 5  # Projets par page
    page_size_query_param = 'page_size'
    max_page_size = 50


class IssuePagination(PageNumberPagination):
    page_size = 3  # Problèmes par page
    page_size_query_param = 'page_size'
    max_page_size = 20


class CommentPagination(PageNumberPagination):
    page_size = 2  # Commentaires par page
    page_size_query_param = 'page_size'
    max_page_size = 10
