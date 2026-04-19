import csv
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

class Command(BaseCommand):
    help = 'Load ingredients from CSV'

    def handle(self, *args, **options):
        with open('data/ingredients.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            ingredients = [Ingredient(name=row[0], measurement_unit=row[1]) for row in reader]
        try:
            Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
        else:
            self.stdout.write(self.style.SUCCESS('Ingredients loaded'))
