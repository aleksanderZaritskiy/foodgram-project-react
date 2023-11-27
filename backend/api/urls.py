from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    RecipeViewSet,
    IngridientViewSet,
    SubscribtionsViewSet,
)


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngridientViewSet)
router.register('users', SubscribtionsViewSet, basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
