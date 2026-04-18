from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeListSerializer,
    RecipeCreateUpdateSerializer, RecipeMinifiedSerializer,
    FavoriteSerializer, ShoppingCartSerializer
)
from .utils import generate_shopping_cart_file


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = RecipeListSerializer

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update', 'update'):
            return RecipeCreateUpdateSerializer
        return RecipeListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        is_favorited = self.request.query_params.get('is_favorited')
        is_in_shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        author_id = self.request.query_params.get('author')
        tags = self.request.query_params.getlist('tags')

        if is_favorited and user.is_authenticated:
            queryset = queryset.filter(favorites__user=user)
        if is_in_shopping_cart and user.is_authenticated:
            queryset = queryset.filter(shopping_cart__user=user)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'], permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': recipe.id}
            serializer = FavoriteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(RecipeMinifiedSerializer(recipe).data, status=status.HTTP_201_CREATED)
        else:
            instance = Favorite.objects.filter(user=request.user, recipe=recipe).first()
            if not instance:
                return Response({'error': 'Рецепт не в избранном'}, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'], permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            data = {'user': request.user.id, 'recipe': recipe.id}
            serializer = ShoppingCartSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(RecipeMinifiedSerializer(recipe).data, status=status.HTTP_201_CREATED)
        else:
            instance = ShoppingCart.objects.filter(user=request.user, recipe=recipe).first()
            if not instance:
                return Response({'error': 'Рецепт не в корзине'}, status=status.HTTP_400_BAD_REQUEST)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        return generate_shopping_cart_file(request.user)

    @action(detail=True, methods=['get'], url_path='get-link')
    def get_short_link(self, request, pk=None):
        get_object_or_404(Recipe, pk=pk)
        full_url = request.build_absolute_uri(f'/recipes/{pk}/')
        return Response({'short-link': full_url})
