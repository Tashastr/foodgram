from django.db import models
from users.models import User

from .constants import (MAX_LEN_TAG, MAX_LEN_INGREDIENT_NAME,
                        MAX_LEN_INGREDIENT_UNIT, MAX_LEN_RECIPE_NAME)


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LEN_TAG,
                            unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=MAX_LEN_TAG, unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LEN_INGREDIENT_NAME,
                            verbose_name='Название')
    measurement_unit = models.CharField(max_length=MAX_LEN_INGREDIENT_UNIT,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор')
    name = models.CharField(max_length=MAX_LEN_RECIPE_NAME,
                            verbose_name='Название')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(verbose_name=(
        'Время приготовления'))
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredients',
                                   verbose_name='Ингредиент')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'], name='unique_recipe_ingredient')]
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites', verbose_name='Рецепт')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_favorite')]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='shopping_cart',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='shopping_cart',
                               verbose_name='Рецепт')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_shopping_cart')]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
