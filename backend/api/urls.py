from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from djoser import views

from .views import (
    TagViewSet,
    RecipeViewSet,
    IngridientViewSet,
    SubscribtionsViewSet,
)


users = DefaultRouter()

users.register('users', views.UserViewSet)

router = DefaultRouter()

router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngridientViewSet)
router.register('users', SubscribtionsViewSet, basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(users.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
