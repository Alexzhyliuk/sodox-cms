from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.home),
    path("home/", views.index, name="index"),
    path("contacts/", views.contacts, name="contacts"),
    path('manufacturers/add/', views.add_manufacturers, name="add_manufacturers"),
    path('categories/add/', views.add_categories, name="add_categories"),
    path('subcategories/add/', views.add_subcategories, name="add_subcategories"),
    path('nomenclatures/add/', views.add_nomenclatures, name="add_nomenclatures"),
    path('nomenclatures_rows/add/', views.add_nomenclatures_rows, name="add_nomenclatures_rows"),
    path('downloads/add/', views.add_downloads, name="add_downloads"),
    path('create_application/', views.CreateApplication.as_view(), name="create_application"),
    path("categories/", views.categories, name="categories"),
    path("category/<int:uid>/", views.category, name="category"),
    path("subcategory/<int:uid>/", views.subcategory, name="subcategory"),
]