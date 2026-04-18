from django.contrib import admin

from .models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Favorite, ShoppingCart
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'cooking_time')
    list_filter = ('tags',)
    search_fields = ('name', 'author__username')
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
    verbose_name = 'Ингредиент рецепта'
    verbose_name_plural = 'Ингредиенты рецептов'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    verbose_name = 'Избранное'
    verbose_name_plural = 'Избранное'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    verbose_name = 'Корзина'
    verbose_name_plural = 'Корзины'
