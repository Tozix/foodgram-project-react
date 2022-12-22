from import_export import resources

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


class IngredientInRecipeResource(resources.ModelResource):
    class Meta:
        model = IngredientInRecipe


class RecipeResource(resources.ModelResource):
    class Meta:
        model = Recipe


class TagResource(resources.ModelResource):
    class Meta:
        model = Tag
