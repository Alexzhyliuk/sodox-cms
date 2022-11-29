from django.contrib import admin
from products.models import *


class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Application, ApplicationAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Manufacturer, ManufacturerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Subcategory, SubcategoryAdmin)


class NomenclatureAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Nomenclature, NomenclatureAdmin)


class NomenclatureRowAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(NomenclatureRow, NomenclatureRowAdmin)


class DownloadsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Downloads, DownloadsAdmin)


class CoordinateAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Coordinate, CoordinateAdmin)

