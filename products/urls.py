from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.home),
    path("home/", views.index, name="index"),
    path("contacts/", views.contacts, name="contacts"),
    path('products/', views.products, name="products"),
    path('products/add/', views.add_products, name="add_products"),
    path('products/characteristics/add/', views.add_products_characteristics, name="add_products_characteristics"),
    path('products/ids/', views.products_ids, name="products_ids"),
    path("product/<int:pk>/", views.ProductDetailsView.as_view(), name="product"),
    path('create_application/', views.CreateApplication.as_view(), name="create_application"),
    path('product/create_order/<int:pk>/', views.CreateOrder.as_view(), name="create_order"),
    path("products/upload/<int:page>", views.json_products, name="upload_products"),
    path("products/subcategory/upload/<int:uid>", views.get_product_in_subcategory, name="upload_products_in_subcategory"),
    path("product/upload/<int:uid>", views.json_product, name="upload_product"),
    path("series/", views.series, name="series")
]