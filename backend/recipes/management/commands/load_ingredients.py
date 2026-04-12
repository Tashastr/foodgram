import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from CSV'

    def handle(self, *args, **options):
        ingredients = []
        with open('data/ingredients.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                name, unit = row
                ingredients.append(Ingredient(name=name, measurement_unit=unit))
        try:
            Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Ingredients loaded'))
