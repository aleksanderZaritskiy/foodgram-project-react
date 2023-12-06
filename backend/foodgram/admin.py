import csv
import json

from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, path
from django.contrib import messages

from .models import (
    Recipe,
    Ingridient,
    Tag,
    RecipeIngridients,
    FavoriteRecipe,
    ShoppingCart,
)
from .forms import ImportFileForm


class ImportFileAdmin:
    """Скрипт для импорта файлов через админ-панель"""

    def upload_file(self, request, model, fields):
        if request.method == 'POST':
            form = ImportFileForm(request.POST, request.FILES)
            format_file = str(request.FILES['file'])
            if form.is_valid():
                with open(
                    f'static/data/{str(request.FILES["file"])}', 'r'
                ) as file:
                    # обработка csv файлов
                    if format_file.endswith('csv'):
                        rows = csv.reader(file, delimiter=',')
                        for row in list(rows):
                            atribute_value = {}
                            for index in range(len(fields)):
                                atribute_value[fields[index]] = row[index]
                            model.objects.update_or_create(**atribute_value)
                    # обработка json файлов
                    else:
                        templates = json.load(file)
                        for atribute_value in templates:
                            model.objects.update_or_create(**atribute_value)
                url = reverse('admin:index')
                messages.success(request, 'Файл успешно импортирован')
                return HttpResponseRedirect(url)
        form = ImportFileForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


class AdminIngridient(admin.ModelAdmin, ImportFileAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ("name",)
    list_display_links = ('name',)
    search_fields = ('name',)

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        return super().upload_file(
            request,
            Ingridient,
            ['name', 'measurement_unit'],
        )


class RecipeIngredientsFormSet(forms.BaseInlineFormSet):

    def clean(self):
        super().clean()
        try:
            if self.cleaned_data:
                pass
        except AttributeError:
            raise forms.ValidationError('Укажите минимум 1 ингредиент')
        if self.deleted_forms:
            for data in self.cleaned_data:
                if data and not data.get('DELETE'):
                    return True
            raise forms.ValidationError(
                'Нужно оставить минимум 1 ингредиент'
            )


class RecipeIngridietInline(admin.TabularInline):
    model = RecipeIngridients
    min_num = 1
    formset = RecipeIngredientsFormSet


class AdminRecipe(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count')
    list_filter = ["name", "author", 'tags']
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = (RecipeIngridietInline,)

    def favorite_count(self, obj):
        return obj.favorite.count()


class ShoppingCartAdmin(admin.ModelAdmin):
    pass


class AdminTag(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )


class AdminFavouriteRecipe(admin.ModelAdmin):
    pass


admin.site.register(Recipe, AdminRecipe)
admin.site.register(Ingridient, AdminIngridient)
admin.site.register(Tag, AdminTag)
admin.site.register(FavoriteRecipe, AdminFavouriteRecipe)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
