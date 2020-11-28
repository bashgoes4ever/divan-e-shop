from .models import *
from django.contrib import admin
# from django import forms
# from django.db.models import Q


# class CategoryForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CategoryForm, self).__init__(*args, **kwargs)
#         self.fields['parent_category'].queryset = Category.objects.filter(~Q(id=self.instance.pk) & Q(level__lte=self.instance.level))


class CategoryAdmin(admin.ModelAdmin):
    exclude = ['level']
    # form = CategoryForm


# class CasingCategoryForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(CasingCategoryForm, self).__init__(*args, **kwargs)
#         self.fields['parent_category'].queryset = CasingCategory.objects.filter(~Q(id=self.instance.pk) & Q(level__lte=self.instance.level))


class CasingCategoryAdmin(admin.ModelAdmin):
    exclude = ['level']
    # form = CasingCategoryForm


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    inlines = [ProductImageInline]
    fieldsets = (
        ('Общая информация', {'fields': ('name', 'catalog_name', 'category', 'description', 'in_stock', 'priority')}),
        ('Цены', {'fields': ('price', 'old_price')}),
        ('Цвета', {'fields': ('casings', 'colors')}),
        ('Размеры', {'fields': ('width', 'depth', 'height', 'bed_width', 'bed_length', 'weight', 'volume')}),
        ('Внешний вид', {'fields': ('frame_material', 'upholstery_material', 'filler_material', 'support_material')}),
        ('Комплектация', {'fields': ('size', 'box', 'has_pillows', 'has_armrests', 'mechanism', 'linings')}),
        ('Особенности', {'fields': ('has_guaranty', 'country', 'features_description')}),
        ('Остальная информация', {'fields': ('similar_products', 'added_to_basket', 'purchased')}),
    )
    search_fields = ('name',)
    ordering = ('price',)

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Mechanism)
admin.site.register(FrameMaterial)
admin.site.register(UpholsteryMaterial)
admin.site.register(FillerMaterial)
admin.site.register(SupportMaterial)
admin.site.register(Country)
admin.site.register(CasingCategory, CasingCategoryAdmin)
admin.site.register(Casing)
admin.site.register(Color)
admin.site.register(CategoryMechanism)