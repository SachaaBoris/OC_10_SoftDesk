"""
Users views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import User
from .serializers import UserDetailSerializer, UserCreateSerializer, UserListSerializer
from .permissions import IsAdminOrSelf, IsAdminOrUnauthenticated
from config.pagination import UserPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les opérations CRUD sur les utilisateurs.
    """
    pagination_class = UserPagination
    
    def get_permissions(self):
        if self.action == 'create':
            # Accès public pour la création de compte
            return [IsAdminOrUnauthenticated()]
        return [IsAuthenticated(), IsAdminOrSelf()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            UserDetailSerializer(user).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Vérifier si l'utilisateur peut modifier ces données
        if not (request.user.is_staff or request.user == instance):
            return Response(
                {"detail": "Vous n'avez pas la permission de modifier cet utilisateur."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Vérifier si l'utilisateur peut supprimer ces données
        if not (request.user.is_staff or request.user == instance):
            return Response(
                {"detail": "Vous n'avez pas la permission de supprimer cet utilisateur."},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Endpoint supplémentaire pour voir le profil"""
        user = self.get_object()
        if not user.can_data_be_shared and not (request.user.is_staff or request.user == user):
            return Response(
                {"detail": "Les données de cet utilisateur ne peuvent pas être partagées."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)