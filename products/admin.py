from django.contrib import admin
from products.models import *


class ApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('phone', 'email', 'message')

admin.site.register(Application, ApplicationAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title',)

admin.site.register(Manufacturer, ManufacturerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title', "manufacturer", "short_description")

admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title', "category")


admin.site.register(Subcategory, SubcategoryAdmin)


class NomenclatureAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title', "subcategory")

admin.site.register(Nomenclature, NomenclatureAdmin)


class NomenclatureRowAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('model', "code", "nomenclature")


admin.site.register(NomenclatureRow, NomenclatureRowAdmin)


class DownloadsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('series', "model", "subcategory")

admin.site.register(Downloads, DownloadsAdmin)


class CoordinateAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('title', "coord_long", "coord_lat")


admin.site.register(Coordinate, CoordinateAdmin)

