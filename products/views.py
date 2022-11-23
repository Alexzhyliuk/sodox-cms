from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from products.models import Coordinate, Application, Product, ProductImage, ProductOrder, ProductCharacteristic, Tag, Manufacturer, Subcategory
from django.views import View
from django.http import JsonResponse
from django.db.models import QuerySet
import math
import csv
import pandas as pd
from django.conf import settings


PRODUCTS_ON_PAGE = 20

def series(request):
    return render(
        request,
        'products/series.html'
    )

def new_application(request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        new_application = Application(name=name, phone=phone, email=email, message=message)
        new_application.save()


def home(request):
	return redirect(reverse("products:index"))


def index(request):
	manufacturers = Manufacturer.objects.all()[:3]
	products = {manufacturer: manufacturer.products.all()[:6] for manufacturer in manufacturers}

	return render(
		request,
		"products/index.html",
		{
			"manufacturers": manufacturers,
			"tabs": products
		}
		)


def contacts(request):
    coords = Coordinate.objects.all()
    return render(
            request,
            "products/contacts.html",
            {
                "coordinates": coords
            }
        )


def products(request):

    subcategory_ids = []
    if "subcategory" in dict(request.GET):
        subcategory_ids = list(map(int, request.GET["subcategory"].split(",")[:-1]))

    manufacturers = Manufacturer.objects.all()

    if subcategory_ids:
        products = Product.objects.all().filter(subcategory__id__in=subcategory_ids)
    else:
        products = Product.objects.all()

    products_count = products.count()
    products = {product: '' for product in products[:PRODUCTS_ON_PAGE]}

    for product in products:
        tags = [tag for tag in product.tags.all()]
        products[product] = tags

    count_of_pages = math.ceil(products_count / PRODUCTS_ON_PAGE)

    return render(
        request,
        'products/products.html',
        {
            "products": products,
            "pages": range(1, count_of_pages + 1),
            "manufacturers": manufacturers,
            "subcategory_ids": subcategory_ids
        } 
    )


def add_products(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_products.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_products.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):
                    print(row[1]["image"])
                    print(type(row[1]["image"]))
                    try:
                        new_product = Product.objects.get_or_create(
                                title=row[1]['title'],
                                price=row[1]['price'],
                                short_description=row[1]['short_desc'],
                                description=row[1]['desc'],
                                image_choice = settings.IMAGE_PATH + str(row[1]['image']),
                                marks=row[1]['marks'],
                                subcategory=Subcategory.objects.get(id=row[1]['subcategory']),
                                manufacturer=Manufacturer.objects.get(id=row[1]['manufacturer']),
                                var1=row[1]['var1'] if str(row[1]['var1']) != 'nan' else '',
                                var2=row[1]['var2'] if str(row[1]['var2']) != 'nan' else '',
                                var3=row[1]['var3'] if str(row[1]['var3']) != 'nan' else '',
                                var4=row[1]['var4'] if str(row[1]['var4']) != 'nan' else '',
                                var5=row[1]['var5'] if str(row[1]['var5']) != 'nan' else '',
                            )
                        # if product has tags
                        if str(row[1]['tags'] ) != 'nan' and new_product[1]:
                            new_product[0].tags.set(str(row[1]['tags']).split(","))

                        if file.shape[1] > 14:
                            for i in range(14, file.shape[1]):
                                if str(row[1][i]) != 'nan':
                                    ProductImage.objects.get_or_create(
                                            title=row[1][i],
                                            image=settings.IMAGES_PATH + str(row[1][i]),
                                            product=new_product[0]
                                        )

                    except Exception as e:
                        print(e)
                        error_rows.append(index+1)

                if error_rows:
                    return render(request, 'products/csv_products.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_products.html', {"message": "Товары успешно добавлены!"})

            return render(request, 'products/csv_products.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            return render(request, 'products/csv_products.html', {"message": "Что-то пошло не так:("})

        return redirect(reverse("products:add_products"))

    return render(
        request,
        'products/csv_products.html',
        {"message": '', "title": "Добавить товары через CSV"}
        )


def add_products_characteristics(request):
    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:
        
        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_products.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_products.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        ProductCharacteristic.objects.get_or_create(
                                product=Product.objects.get(id=row[1]['product']),
                                model=row[1]['model'],
                                code=row[1]['code'],
                                description=row[1]['desc'],
                                var1=row[1]['var1'] if str(row[1]['var1']) != 'nan' else '',
                                var2=row[1]['var2'] if str(row[1]['var2']) != 'nan' else '',
                                var3=row[1]['var3'] if str(row[1]['var3']) != 'nan' else '',
                                var4=row[1]['var4'] if str(row[1]['var4']) != 'nan' else '',
                                var5=row[1]['var5'] if str(row[1]['var5']) != 'nan' else '',
                            )
                    except Exception as e:
                        print(e)
                        error_rows.append(index+1)

                if error_rows:
                    return render(request, 'products/csv_products.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_products.html', {"message": "Характеристики успешно добавлены!"})

            return render(request, 'products/csv_products.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            print(e)
            return render(request, 'products/csv_products.html', {"message": "Что-то пошло не так:("})

        return redirect(reverse("products:add_products_characteristics"))

    return render(
        request,
        'products/csv_products.html',
        {"message": '', "title": "Добавить характеристики через CSV"}
        )


def products_ids(request):

    products = Product.objects.all().values('title', 'id')

    return render(
        request,
        'products/products_ids.html',
        {
            "products": products
        }
        )

class ProductDetailsView(DetailView):
    model = Product
    template_name = "products/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manufacturers = Manufacturer.objects.all()
        other_products = Product.objects.all().filter(manufacturer=context['object'].manufacturer)[:20]
        active_vars = context['object'].get_vars()
        characteristic = context['object'].characteristic.all()

        context['manufacturers'] = manufacturers
        context['other_products'] = other_products
        context['vars'] = active_vars
        context['characteristic'] = characteristic
        context['characteristic_model'] = ProductCharacteristic

        return context


class CreateApplication(View):
    def post(self, request, *args, **kwargs):

        new_application(request)
        
        return redirect(reverse("products:index"))


class CreateOrder(View):
    def post(self, request, *args, **kwargs):

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")
        product = Product.objects.get(id=kwargs['pk'])

        new_order = ProductOrder(name=name, phone=phone, email=email, message=message, product=product)
        new_order.save()

        return redirect(reverse("products:product", kwargs={"pk": kwargs['pk']}))


def json_product(request, uid):

    product = Product.objects.get(id=uid)

    return JsonResponse({
        "product": {
                "id": product.id,
                "image": product.get_image_url(),
                "title": product.title,
                "tags": [
                    {
                        "title": tag.title,
                        "color": tag.color
                    }
                    for tag in product.tags.all()
                ]
            }
        })


def json_products(request, page):

    subcategory_ids = []
    if "subcategory" in dict(request.GET):
        subcategory_ids = list(map(int, request.GET["subcategory"].split(",")[:-1]))

    if subcategory_ids:
        products = Product.objects.all().filter(subcategory__id__in=subcategory_ids)[0+((page-1) * PRODUCTS_ON_PAGE):PRODUCTS_ON_PAGE+((page-1) * PRODUCTS_ON_PAGE)]

    else:
        products = Product.objects.all()[0+((page-1) * PRODUCTS_ON_PAGE):PRODUCTS_ON_PAGE+((page-1) * PRODUCTS_ON_PAGE)]

    return JsonResponse({
        "products": [
            {
                "id": product.id,
                "image": product.get_image_url(),
                "title": product.title,
                "price": product.price,
                "tags": [
                    {
                        "title": tag.title,
                        "color": tag.color
                    }
                    for tag in product.tags.all()
                ],
                "subcategory": product.subcategory.id
            }
            for product in products
        ]
    })


def get_product_in_subcategory(request, uid):
    subcategory = Subcategory.objects.get(id=uid)
    products = Product.objects.all().filter(subcategory=subcategory)

    return JsonResponse({
        "products": [
            {
                "id": product.id,
                "image": product.get_image_url(),
                "title": product.title,
                "price": product.price,
                "tags": [
                    {
                        "title": tag.title,
                        "color": tag.color
                    }
                    for tag in product.tags.all()
                ],
                "subcategory": uid
            } for product in products
        ]
    })


