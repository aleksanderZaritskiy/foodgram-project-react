import os
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from .filters import RecipeFilter
from .permissions import IsAnyReadUserPostorAuthorUpdateRecipePermissions
from foodgram.models import (
    Tag,
    Recipe,
    ShoppingCart,
    Ingridient,
    FavouriteRecipe,
    Subscribe,
)
from users.models import User
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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """Recipe view"""
    
    queryset = Recipe.objects.all()
    serializer_class = WriteRecipeSrializer
    permission_classes = (IsAnyReadUserPostorAuthorUpdateRecipePermissions,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def favorite(self, request, pk):
        get_favorite_recipe = FavouriteRecipe.objects.filter(
            recipe_id=pk, user=request.user
        )
        if request.method == 'POST':
            if get_favorite_recipe.exists():
                return Response(
                    {'response': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = get_object_or_404(Recipe, id=pk)
            FavouriteRecipe.objects.create(recipe=recipe, user=request.user)
            return Response(
                FavouriteShoppingCardSerializer(
                    recipe, context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED,
            )
        if get_favorite_recipe.exists():
            get_favorite_recipe.delete()
            return Response(
                {'response': 'Рецепт удален из избранного'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'error': 'рецепта нет в избранном'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        get_shopping_cart = ShoppingCart.objects.filter(
            recipe_id=pk, user=request.user
        )
        if request.method == 'POST':
            if get_shopping_cart.exists():
                return Response(
                    {'response': 'Рецепт уже в корзине'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.create(recipe=recipe, user=request.user)
            return Response(
                FavouriteShoppingCardSerializer(
                    recipe, context={'request': request}
                ).data,
                status=status.HTTP_201_CREATED,
            )
        if get_shopping_cart.exists():
            get_shopping_cart.delete()
            return Response(
                {'response': 'Рецепт удален из корзины'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'error': 'рецепта нет в корзине'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def download_shopping_cart(self, request):
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
        recipes = Recipe.objects.filter(shopping_cart__user=request.user)
        for recipe in recipes:
            tmp_ingredients = recipe.recipes.values(
                'ingredients__name', 'ingredients__measurement_unit'
            ).annotate(sum_amount=Sum('amount'))
            reject = 700
            for ingredients in tmp_ingredients:
                name = ingredients['ingredients__name']
                m_unit = ingredients['ingredients__measurement_unit']
                amount = ingredients['sum_amount']
                file.drawString(100, reject, f'*{name}, ({m_unit}) — {amount}')
                reject += 15
        file.showPage()
        file.save()
        return response


class SubscriptionsListViewSet(ListModelMixin, GenericViewSet):
    serializer_class = SubscriptionsListSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_user(self):
        return get_object_or_404(User, username=self.request.user)

    def get_queryset(self):
        return self.get_user().user.all()


class SubscriptionsCreateDeleteViewSet(
    CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = Subscribe.objects.all()
    serializer_class = SubscriptionsCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(methods=['POST', 'DELETE'], detail=True)
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
