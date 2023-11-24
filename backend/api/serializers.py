from djoser.serializers import UserSerializer as BaseUserSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers


from users.models import User
from foodgram.models import (
    Tag,
    Recipe,
    RecipeIngridients,
    Ingridient,
    Subscribe,
    FavouriteRecipe,
    ShoppingCart,
)


class GetUserSerializer(BaseUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        return all(
            (
                (not current_user.is_anonymous),
                Subscribe.objects.filter(
                    user=current_user.id, subscriber=obj.id
                ).exists(),
            )
        )


class CreateUserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        #read_only_fields = ('id', 'name', 'color', 'slug')


class IngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingridient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = ('id', 'name', 'measurement_unit')


class RecipeIngridientsSerializer(serializers.ModelSerializer):
    """Сериалайзер для чтения Рецепта"""

    id = serializers.PrimaryKeyRelatedField(
        source='ingredients.id', queryset=Ingridient.objects.all()
    )
    measurement_unit = serializers.CharField(
        source='ingredients.measurement_unit', read_only=True
    )
    name = serializers.CharField(source='ingredients.name', read_only=True)

    class Meta:
        model = RecipeIngridients
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class GetIngredientserializer(serializers.ModelSerializer):
    """Сериалайзер для создания Рецепта"""

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngridients
        fields = ('id', 'amount')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Чтение рецептов"""

    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    author = GetUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngridients.objects.filter(recipe_id=obj.id)
        return RecipeIngridientsSerializer(ingredients, many=True).data

    def _get_favorite_shopping_cart(self, user, model, obj):
        return all(
            (
                (not user.is_anonymous),
                model.objects.filter(user=user.id, recipe=obj.id).exists(),
            )
        )

    def get_is_favorited(self, obj):
        return self._get_favorite_shopping_cart(
            self.context.get('request').user, FavouriteRecipe, obj
        )

    def get_is_in_shopping_cart(self, obj):
        return self._get_favorite_shopping_cart(
            self.context.get('request').user, ShoppingCart, obj
        )


class WriteRecipeSrializer(serializers.ModelSerializer):

    """Изменение рецептов"""

    image = Base64ImageField(required=True)
    ingredients = GetIngredientserializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'image',
            'name',
            'text',
            'cooking_time',
            'tags',
            'ingredients',
        )
        read_only_fields = ('author',)

    def to_representation(self, instance):
        request = self.context.get('request')
        serializer = ReadRecipeSerializer(
            instance, context={'request': request}
        )
        return serializer.data

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        id_ingredients = []
        for ingredient in ingredients:
            current_ingredient_id = ingredient.get('id')
            if not Ingridient.objects.filter(
                id=current_ingredient_id
            ).exists():
                raise serializers.ValidationError('Такого нет ингредиента')
            if current_ingredient_id in id_ingredients:
                raise serializers.ValidationError(
                    'Уберите дублирующиеся ингредиенты'
                )
            id_ingredients.append(current_ingredient_id)
        return data

    def create(self, validated_data):
        if (
            'ingredients' not in self.initial_data
            or 'tags' not in self.initial_data
        ):
            raise serializers.ValidationError(
                {'detail': 'Нужно заполнить поля ingredients/tags'}
            )
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags_data)
        for data in ingredients_data:
            RecipeIngridients.objects.create(
                recipe=recipe,
                ingredients=Ingridient.objects.get(id=data.get('id')),
                amount=data.get('amount'),
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.text = validated_data.get('text', instance.text)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            instance.tags.set(tags_data)
        if 'ingredients' in validated_data:
            instance.ingredients.clear()
            ingredients_data = validated_data.pop('ingredients')

            for data in ingredients_data:
                RecipeIngridients.objects.create(
                    recipe=instance,
                    ingredients=Ingridient.objects.get(id=data.get('id')),
                    amount=data.get('amount'),
                )
        return instance


class FavouriteShoppingCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class SubscriptionsListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='subscriber.id', queryset=User.objects.all()
    )
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(source='subscriber.email', read_only=True)
    first_name = serializers.CharField(
        source='subscriber.first_name', read_only=True
    )
    last_name = serializers.CharField(
        source='subscriber.last_name', read_only=True
    )
    username = serializers.CharField(
        source='subscriber.username', read_only=True
    )

    class Meta:
        model = Subscribe
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        return Subscribe.objects.filter(
            user=obj.user, subscriber=obj.subscriber
        ).count()

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(
            user=obj.user, subscriber=obj.subscriber
        ).exists()

    def get_recipes(self, obj):
        request = self.context['request']
        recipe_limit = request.query_params.get('recipes_limit')
        recipe = Recipe.objects.filter(author=obj.subscriber)
        if recipe_limit:
            recipe = recipe[:int(recipe_limit)]
        return FavouriteShoppingCardSerializer(recipe, many=True).data


class SubscriptionsCreateSerializer(serializers.ModelSerializer):
    user = (
        serializers.SlugRelatedField(
            slug_field='id',
            read_only=True,
        ),
    )
    subscriber = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True,
    )

    class Meta:
        model = Subscribe
        fields = (
            'user',
            'subscriber',
        )
        read_only_fields = (
            'user',
            'subscriber',
        )