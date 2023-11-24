from django.urls import path, include, re_path
from djoser import views
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    RecipeViewSet,
    IngridientViewSet,
    SubscriptionsListViewSet,
    SubscriptionsCreateDeleteViewSet,
)


users = DefaultRouter()
users.register('users', views.UserViewSet, basename='users')

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngridientViewSet)
router.register(
    'users', SubscriptionsCreateDeleteViewSet, basename='subscribe'
)


urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionsListViewSet.as_view({'get': 'list'}),
        name='subscriptions',
    ),
    path('', include(users.urls)),
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
