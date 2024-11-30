"""
Provides custom permissions.
"""
from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission autorisant uniquement l'admin ou l'utilisateur lui-même
    """
    def has_permission(self, request, view):
        # Admins peuvent tout faire
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        # Pour les opérations de création (POST)
        if view.action == 'create':
            return True

        # Pour l'action GET 'userlist'
        if view.action == 'list':
            return request.user.is_authenticated

        # Pour les autres opérations, vérifier l'ID de l'utilisateur
        if 'pk' in view.kwargs:
            return str(request.user.pk) == str(view.kwargs['pk'])
        
        return False

    def has_object_permission(self, request, view, obj):
        # Admins peuvent tout faire
        if request.user.is_staff or request.user.is_superuser:
            return True
            
        # L'utilisateur ne peut accéder qu'à ses propres données
        return obj == request.user


class IsAdminOrUnauthenticated(permissions.BasePermission):
    """
    Permission pour les utilisateurs non authentifiés ou les admins à créer un nouvel utilisateur.
    """
    def has_permission(self, request, view):
        # Autorise si l'utilisateur est non authentifié (i.e., pas de user dans request.user)
        if not request.user.is_authenticated:
            print("Utilisateur non authentifié - Accès autorisé")
            return True
        
        # Autorise si l'utilisateur est admin (staff ou superuser)
        if request.user.is_staff or request.user.is_superuser:
            print("Admin user - Accès autorisé")
            return True
        
        return False