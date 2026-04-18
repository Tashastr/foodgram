from django.http import HttpResponse

from .models import Recipe


def generate_shopping_cart_file(user):
    recipes = Recipe.objects.filter(shopping_cart__user=user)
    ingredients = {}
    for recipe in recipes:
        for recipe_ingredient in recipe.recipe_ingredients.all():
            key = (f"{recipe_ingredient.ingredient.name} "
                   f"({recipe_ingredient.ingredient.measurement_unit})")
            ingredients[key] = (
                ingredients.get(key, 0) + recipe_ingredient.amount
            )
    lines = [f"{name} — {amount}" for name, amount in ingredients.items()]
    content = "\n".join(lines)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.txt"'
    )
    return response
