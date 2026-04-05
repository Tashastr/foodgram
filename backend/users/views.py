from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Follow
from .serializers import CustomUserSerializer
from recipes.serializers import RecipeMinifiedSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'], 
permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], url_path='subscribe', 
permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, pk=None):
        author = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            if request.user == author:
                return Response({'error': 'You cannot subscribe to yourself.'}, 
status=status.HTTP_400_BAD_REQUEST)
            follow, created = Follow.objects.get_or_create(user=request.user, 
author=author)
            if not created:
                return Response({'error': 'Already subscribed.'}, 
status=status.HTTP_400_BAD_REQUEST)
            serializer = CustomUserSerializer(author, context={'request': 
request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            follow = Follow.objects.filter(user=request.user, author=author)
            if not follow.exists():
                return Response({'error': 'Not subscribed.'}, 
status=status.HTTP_400_BAD_REQUEST)
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
