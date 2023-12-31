import os

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .paginations import LimitPageNumberPagination
from .filters import RecipeFilter, IngredientSearchFilter
from .permissions import GreateOrUpdateOrReadOnlyRecipePermissions
from foodgram.models import (
    Tag,
    Recipe,
    ShoppingCart,
    Ingridient,
    FavoriteRecipe,
)
from users.models import User, Subscribe
from .serializers import (
    TagSerializer,
    WriteRecipeSrializer,
    IngridientSerializer,
    FavouriteShoppingCardSerializer,
    SubscriptionsListSerializer,
    SubscriptionsCreateSerializer,
)


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Tag view"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    lookup_field = 'id'


class IngridientViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Ingredient view"""

    queryset = Ingridient.objects.all()
    serializer_class = IngridientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe view"""

    queryset = Recipe.objects.all()
    serializer_class = WriteRecipeSrializer
    permission_classes = (GreateOrUpdateOrReadOnlyRecipePermissions,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def _favorite_or_shopping_cart_request(self, request, model, id, detail):
        get_object = model.objects.filter(
            recipe_id=id,
            user=request.user,
        )
        if request.method == 'POST':
            if get_object.exists():
                return Response(
                    {'response': detail['exists']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = get_object_or_404(Recipe, id=id)
            model.objects.create(recipe=recipe, user=request.user)
            return Response(
                FavouriteShoppingCardSerializer(
                    recipe, context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED,
            )
        if get_object.exists():
            get_object.delete()
            return Response(
                {'response': detail['delete_accept']},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'response': detail['delete_denied']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        return self._favorite_or_shopping_cart_request(
            request,
            FavoriteRecipe,
            pk,
            {
                'exists': 'Рецепт уже в избранном',
                'delete_accept': 'Рецепт удалён',
                'delete_denied': 'Рецепта нет в избранном',
            },
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        return self._favorite_or_shopping_cart_request(
            request,
            ShoppingCart,
            pk,
            {
                'exists': 'Рецепт уже в корзине',
                'delete_accept': 'Рецепт удалён',
                'delete_denied': 'Рецепта нет в корзине',
            },
        )

    def get_pdf(self, ingredients):
        """Отрисовка pdf файла"""
        response = HttpResponse(content_type='application/pdf')
        response[
            'Content-Disposition'
        ] = 'Список покупок; filename="shopping_cart.pdf"'
        file = Canvas(response)
        fonts = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'font_files/',
            'Verdana.ttf',
        )
        pdfmetrics.registerFont(TTFont('Verdana', fonts))
        file.setFont("Verdana", 15)
        index = len(ingredients)
        for name in ingredients:
            file.drawString(
                100,
                ingredients[name]['reject'],
                f'{index}) {name} ({ingredients[name]["m_unit"]})'
                f' — {ingredients[name]["amount"]}',
            )
            index -= 1
        file.showPage()
        file.save()
        return response

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        recipes = Recipe.objects.filter(shopping_cart__user=request.user)
        reject = 700
        ingredients_data = {}
        for recipe in recipes:
            tmp_ingredients = recipe.ingredients.values(
                'ingredients__name',
                'ingredients__measurement_unit',
                'amount',
            )
            for ingredients in tmp_ingredients:
                name = ingredients['ingredients__name']
                if name in ingredients_data:
                    amount = ingredients['amount']
                    ingredients_data[name]['amount'] += amount
                else:
                    m_unit = ingredients['ingredients__measurement_unit']
                    amount = ingredients['amount']
                    ingredients_data[name] = {
                        'reject': reject,
                        'm_unit': m_unit,
                        'amount': amount,
                    }
                reject += 30
        return self.get_pdf(ingredients_data)


class SubscribtionsViewSet(
    GenericViewSet,
):
    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        pagination_class=LimitPageNumberPagination,
    )
    def subscriptions(self, request):
        current_user = get_object_or_404(User, username=request.user)
        subscribtions_list = current_user.user.all()
        page = self.paginate_queryset(subscribtions_list)
        serializer = SubscriptionsListSerializer(
            page,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, pk):
        try:
            check_subsribing = Subscribe.objects.filter(
                user=self.request.user, subscriber=User.objects.get(id=pk)
            )
        except ObjectDoesNotExist:
            return Response(
                {'default': 'такой пользователь не существует'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if request.method == 'POST':
            if self.request.user.id == int(pk):
                return Response(
                    {'default': 'Нельзя подписаться на себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscriber = get_object_or_404(User, id=pk)
            if check_subsribing.exists():
                return Response(
                    {'default': 'Вы уже подписаны'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscribing = Subscribe.objects.create(
                user=self.request.user,
                subscriber=subscriber,
            )
            serializer = SubscriptionsCreateSerializer(
                subscribing,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if check_subsribing.exists():
            check_subsribing.delete()
            return Response(
                {'default': 'Вы отписались'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'error': 'Вы не подписаны на пользователя'},
            status=status.HTTP_400_BAD_REQUEST,
        )
