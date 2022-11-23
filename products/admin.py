from django.contrib import admin
from products.models import Application, Product, ProductOrder, ProductCharacteristic, ProductImage, Tag, Manufacturer, Overcategory, Category, Subcategory, Coordinate


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Product, ProductAdmin)


class ProductCharacteristicAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(ProductCharacteristic, ProductCharacteristicAdmin)


class ProductOrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(ProductOrder, ProductOrderAdmin)


class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Application, ApplicationAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(ProductImage, ProductImageAdmin)


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Tag, TagAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Manufacturer, ManufacturerAdmin)


class OvercategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Overcategory, OvercategoryAdmin)


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Subcategory, SubcategoryAdmin)


class CoordinateAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Coordinate, CoordinateAdmin)

