import base64
from django.core.files.base import ContentFile
from rest_framework import serializers
from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart
)
from users.serializers import CustomUserSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientInRecipeSerializer(source='recipeingredient_set',
                                               many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user,
                                           recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return ShoppingCart.objects.filter(user=request.user,
                                               recipe=obj).exists()
        return False


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    ingredients = serializers.ListField(write_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time')

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "Ingredients list cannot be empty.")
        for item in value:
            if 'id' not in item or 'amount' not in item:
                raise serializers.ValidationError(
                    "Each ingredient must have id and amount.")
            if not Ingredient.objects.filter(id=item['id']).exists():
                raise serializers.ValidationError(
                    f"Ingredient with id {item['id']} does not exist.")
            if item['amount'] < 1:
                raise serializers.ValidationError("Amount must be at least 1.")
        return value

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ing_data in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ing_data['id'],
                amount=ing_data['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.set(tags)
        if ingredients_data is not None:
            instance.recipeingredient_set.all().delete()
            for ing_data in ingredients_data:
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient_id=ing_data['id'],
                    amount=ing_data['amount']
                )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data
