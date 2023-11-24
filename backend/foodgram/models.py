from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_time
from .constants import LENGTH_NAME_OBJ, LENGTH_COLOR

User = get_user_model()


class NameObjects(models.Model):
    """Абстрактный класс"""

    name = models.CharField(
        'Название',
        help_text='Укажите название',
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )

    class Meta:
        abstract = True


class Tag(NameObjects):
    """Модель Тега"""

    color = models.CharField(
        'Цвет',
        help_text='Укажите цвет',
        max_length=LENGTH_COLOR,
        null=True,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        help_text='Укажите слаг, поле должно быть уникальным',
        max_length=LENGTH_NAME_OBJ,
        unique=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ingridient(NameObjects):
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=LENGTH_NAME_OBJ,
        help_text='Укажите единицу измерения',
    )
    name = models.CharField(
        'Название',
        help_text='Укажите название',
        max_length=LENGTH_NAME_OBJ,
    )

    class Meta:
        verbose_name_plural = 'Ingridients'

    def __str__(self):
        return self.name


class Recipe(NameObjects):
    """Модель рецепта"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        'Фотография',
        help_text='Добавьте фотографию рецепта',
    )
    text = models.TextField(
        'Описание рецепта',
        help_text='Опишите рецепт',
    )
    ingredients = models.ManyToManyField(
        Ingridient,
        through='RecipeIngridients',
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Укажите время приготовления',
        validators=(validate_time,),
    )

    class Meta:
        verbose_name_plural = 'Recipes'
        default_related_name = 'recipe'

    def __str__(self):
        return self.name


class RecipeIngridients(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipes'
    )
    ingredients = models.ForeignKey(
        Ingridient, on_delete=models.CASCADE, related_name='ingridient'
    )
    amount = models.SmallIntegerField('Колличество')


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name_plural = 'FavouriteRecipes'
        default_related_name = 'favourite'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favourite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        default_related_name = 'shopping_cart'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_purchase'
            )
        ]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user'
    )
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriber'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'], name='unique_subscribe'
            )
        ]


class ImportFile(models.Model):
    file = models.FileField(upload_to='uploads/')
