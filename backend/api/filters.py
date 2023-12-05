import django_filters

from foodgram.models import Recipe, Ingridient
from users.models import User


class IngredientSearchFilter(django_filters.rest_framework.FilterSet):
    name = django_filters.rest_framework.CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingridient
        fields = ('name',)


class RecipeFilter(django_filters.rest_framework.FilterSet):
    author = django_filters.rest_framework.ModelChoiceFilter(
        queryset=User.objects.all()
    )
    tags = django_filters.rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug'
    )
    is_favorited = django_filters.rest_framework.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = django_filters.rest_framework.BooleanFilter(
        method='get_recipe_in_shopping_cart'
    )

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def get_recipe_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )
