from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from products.models import *
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import QuerySet
import math
import csv
import pandas as pd
from django.conf import settings


def categories(request):
    manufacturers = { manufacturer: manufacturer.categories.all()[:6] if i < 4 else [] for i, manufacturer in enumerate(Manufacturer.objects.all().order_by("id"), 1) }

    return render(
        request,
        'products/categories.html',
        {
            "manufacturers": manufacturers,
        }
    )

def category(request, uid):
    category = Category.objects.get(id=uid)
    manufacturers = Manufacturer.objects.all().order_by("id")
    return render(
        request,
        'products/category.html',
        {
            "category": category,
            "manufacturers": manufacturers,
        }
    )


def subcategory(request, uid):
    subcategory = Subcategory.objects.get(id=uid)
    manufacturers = Manufacturer.objects.all().order_by("id")
    if Nomenclature.objects.filter(subcategory=subcategory).exists():
        nomenclature = subcategory.nomenclature
    else:
        nomenclature = None

    return render(
        request,
        'products/subcategory.html',
        {
            "subcategory": subcategory,
            "manufacturers": manufacturers,
            "nomenclature": nomenclature,
        }
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
	return render(
		request,
		"products/index.html",
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


# def upload_csv(funct):
#     def wrapper(request):
#         if not(request.user.is_superuser):
#             return redirect(reverse("products:index"))

#         if request.POST:

#             try:

#                 data = request.FILES.get("csv_file")

#                 if data:

#                     csv_file = request.FILES['csv_file']
#                     if not csv_file.name.endswith('.csv'):
#                         return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

#                     try:
#                         if request.POST.get('sep'):
#                             file = pd.read_csv(csv_file, sep=';')
#                         else:
#                             file = pd.read_csv(csv_file)

#                     except Exception as e:
#                         print(e)
#                         return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})

#                     error_rows = []
#                     for index, row in enumerate(file.iterrows()):

#                         try:
#                             funct(request, row)

#                         except Exception as e:
#                             print(e)
#                             error_rows.append(index+1)

#                     if error_rows:
#                         return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

#                     return render(request, 'products/csv_upload.html', {"message": "Производители успешно добавлены!"})

#                 return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


#             except Exception as e:
#                 return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

#         return render(
#             request,
#             'products/csv_upload.html',
#             {"message": '', "title": "Добавить производителей через CSV"}
#             )

#     return wrapper

# @upload_csv
# def add_manufacturers(request, row=[]):

#     Manufacturer.objects.get_or_create(
#             title=row[1]['title'],
#             image=settings.MANUFACTURER_IMAGE_PATH + str(row[1]['image']),
#             inactive_image=settings.MANUFACTURER_IMAGE_PATH + str(row[1]['inactive_image']),
#         )




def add_manufacturers(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        Manufacturer.objects.get_or_create(
                                title=row[1]['title'],
                                image=settings.MANUFACTURER_IMAGE_PATH + str(row[1]['image']),
                                inactive_image=settings.MANUFACTURER_IMAGE_PATH + str(row[1]['inactive_image']),
                            )

                    except Exception as e:
                        print(e)
                        error_rows.append(index+1)

                if error_rows:
                    return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_upload.html', {"message": "Производители успешно добавлены!"})

            return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

    return render(
        request,
        'products/csv_upload.html',
        {"message": '', "title": "Добавить производителей через CSV"}
        )


def add_categories(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        Category.objects.get_or_create(
                                manufacturer = Manufacturer.objects.filter(title=str(row[1]['manufacturer'])).first(),
                                title=row[1]['title'],
                                image=settings.CATEGORY_IMAGE_PATH + str(row[1]['image']),
                                short_description=row[1]["short_description"],
                                description=row[1]["description"],
                                advantages=row[1]["advantages"],
                                recommendation=row[1]["recommendation"],
                            )

                    except Exception as e:
                        print(e)
                        error_rows.append(index+1)

                if error_rows:
                    return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_upload.html', {"message": "Категории успешно добавлены!"})

            return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            print(e)
            return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

    return render(
        request,
        'products/csv_upload.html',
        {"message": '', "title": "Добавить категории через CSV"}
        )


def add_subcategories(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        Subcategory.objects.get_or_create(
                                category = Category.objects.filter(title=str(row[1]['category']), manufacturer__title=str(row[1]["manufacturer"])).first(),
                                title=row[1]['title'],
                                image=settings.SUBCATEGORY_IMAGE_PATH + str(row[1]['image']),
                                description=row[1]["description"],
                                review=row[1]["review"],
                            )

                    except Exception as e:
                        print(e)
                        error_rows.append(index+1)

                if error_rows:
                    return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_upload.html', {"message": "Подкатегории успешно добавлены!"})

            return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            print(e)
            return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

    return render(
        request,
        'products/csv_upload.html',
        {"message": '', "title": "Добавить подкатегории через CSV"}
        )


def add_nomenclatures(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        Nomenclature.objects.get_or_create(
                                subcategory = Subcategory.objects.filter(title=str(row[1]['subcategory'])).filter(category__title=str(row[1]["category"])).filter(category__manufacturer__title=str(row[1]["manufacturer"])).first(),
                                title=row[1]['title'],
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
                    return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_upload.html', {"message": "Номенклатуры успешно добавлены!"})

            return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            print(e)
            return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

    return render(
        request,
        'products/csv_upload.html',
        {"message": '', "title": "Добавить номенклатуры через CSV"}
        )


def add_nomenclatures_rows(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        NomenclatureRow.objects.get_or_create(
                                nomenclature = Nomenclature.objects.get(title=str(row[1]['nomenclature'])) if Nomenclature.objects.filter(title=str(row[1]['nomenclature'])).count() == 1 else -1,
                                model=row[1]['model'],
                                code=row[1]['code'],
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
                    return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_upload.html', {"message": "Строки для номенклатур успешно добавлены!"})

            return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            print(e)
            return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

    return render(
        request,
        'products/csv_upload.html',
        {"message": '', "title": "Добавить строки для номенклатур через CSV"}
        )


def add_downloads(request):

    if not(request.user.is_superuser):
        return redirect(reverse("products:index"))

    if request.POST:

        try:

            data = request.FILES.get("csv_file")

            if data:

                csv_file = request.FILES['csv_file']
                if not csv_file.name.endswith('.csv'):
                    return render(request, 'products/csv_upload.html', {"message": "Загружен не csv файл!"})

                try:
                    if request.POST.get('sep'):
                        file = pd.read_csv(csv_file, sep=';')
                    else:
                        file = pd.read_csv(csv_file)

                except Exception as e:
                    print(e)
                    return render(request, 'products/csv_upload.html', {"message": "Неверный разделитель"})


                error_rows = []
                for index, row in enumerate(file.iterrows()):

                    try:
                        Downloads.objects.get_or_create(
                                subcategory = Subcategory.objects.filter(title=str(row[1]['subcategory'])).filter(category__title=str(row[1]["category"])).filter(category__manufacturer__title=str(row[1]["manufacturer"])).first(),
                                series=row[1]['series'],
                                model=row[1]['model'],
                                file=settings.DOWNLOADS_FILE_PATH + str(row[1]["file"]),
                            )

                    except Exception as e:
                        print(e)
                        error_rows.append(index+1)

                if error_rows:
                    return render(request, 'products/csv_upload.html', {"message": f"Ошибки в строках {error_rows}"})

                return render(request, 'products/csv_upload.html', {"message": "Файлы для скачивания успешно добавлены!"})

            return render(request, 'products/csv_upload.html', {"message": "Проблема с файлом!"})


        except Exception as e:
            print(e)
            return render(request, 'products/csv_upload.html', {"message": "Что-то пошло не так:("})

    return render(
        request,
        'products/csv_upload.html',
        {"message": '', "title": "Добавить файлы для скачивания через CSV"}
        )

# def add_products_characteristics(request):
#     if not(request.user.is_superuser):
#         return redirect(reverse("products:index"))

#     if request.POST:
        
#         try:

#             data = request.FILES.get("csv_file")

#             if data:

#                 csv_file = request.FILES['csv_file']
#                 if not csv_file.name.endswith('.csv'):
#                     return render(request, 'products/csv_products.html', {"message": "Загружен не csv файл!"})

#                 try:
#                     if request.POST.get('sep'):
#                         file = pd.read_csv(csv_file, sep=';')
#                     else:
#                         file = pd.read_csv(csv_file)

#                 except Exception as e:
#                     print(e)
#                     return render(request, 'products/csv_products.html', {"message": "Неверный разделитель"})


#                 error_rows = []
#                 for index, row in enumerate(file.iterrows()):

#                     try:
#                         ProductCharacteristic.objects.get_or_create(
#                                 product=Product.objects.get(id=row[1]['product']),
#                                 model=row[1]['model'],
#                                 code=row[1]['code'],
#                                 description=row[1]['desc'],
#                                 var1=row[1]['var1'] if str(row[1]['var1']) != 'nan' else '',
#                                 var2=row[1]['var2'] if str(row[1]['var2']) != 'nan' else '',
#                                 var3=row[1]['var3'] if str(row[1]['var3']) != 'nan' else '',
#                                 var4=row[1]['var4'] if str(row[1]['var4']) != 'nan' else '',
#                                 var5=row[1]['var5'] if str(row[1]['var5']) != 'nan' else '',
#                             )
#                     except Exception as e:
#                         print(e)
#                         error_rows.append(index+1)

#                 if error_rows:
#                     return render(request, 'products/csv_products.html', {"message": f"Ошибки в строках {error_rows}"})

#                 return render(request, 'products/csv_products.html', {"message": "Характеристики успешно добавлены!"})

#             return render(request, 'products/csv_products.html', {"message": "Проблема с файлом!"})


#         except Exception as e:
#             print(e)
#             return render(request, 'products/csv_products.html', {"message": "Что-то пошло не так:("})

#         return redirect(reverse("products:add_products_characteristics"))

#     return render(
#         request,
#         'products/csv_products.html',
#         {"message": '', "title": "Добавить характеристики через CSV"}
#         )


# def products_ids(request):

#     products = Product.objects.all().values('title', 'id')

#     return render(
#         request,
#         'products/products_ids.html',
#         {
#             "products": products
#         }
#         )

# class ProductDetailsView(DetailView):
#     model = Product
#     template_name = "products/product.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         manufacturers = Manufacturer.objects.all()
#         other_products = Product.objects.all().filter(manufacturer=context['object'].manufacturer)[:20]
#         active_vars = context['object'].get_vars()
#         characteristic = context['object'].characteristic.all()

#         context['manufacturers'] = manufacturers
#         context['other_products'] = other_products
#         context['vars'] = active_vars
#         context['characteristic'] = characteristic
#         context['characteristic_model'] = ProductCharacteristic

#         return context


class CreateApplication(View):
    def post(self, request, *args, **kwargs):

        new_application(request)
        
        return redirect(reverse("products:index"))


# class CreateOrder(View):
#     def post(self, request, *args, **kwargs):

#         name = request.POST.get("name")
#         phone = request.POST.get("phone")
#         email = request.POST.get("email")
#         message = request.POST.get("message")
#         product = Product.objects.get(id=kwargs['pk'])

#         new_order = ProductOrder(name=name, phone=phone, email=email, message=message, product=product)
#         new_order.save()

#         return redirect(reverse("products:product", kwargs={"pk": kwargs['pk']}))


# def json_product(request, uid):

#     product = Product.objects.get(id=uid)

#     return JsonResponse({
#         "product": {
#                 "id": product.id,
#                 "image": product.get_image_url(),
#                 "title": product.title,
#                 "tags": [
#                     {
#                         "title": tag.title,
#                         "color": tag.color
#                     }
#                     for tag in product.tags.all()
#                 ]
#             }
#         })


# def json_products(request, page):

#     subcategory_ids = []
#     if "subcategory" in dict(request.GET):
#         subcategory_ids = list(map(int, request.GET["subcategory"].split(",")[:-1]))

#     if subcategory_ids:
#         products = Product.objects.all().filter(subcategory__id__in=subcategory_ids)[0+((page-1) * PRODUCTS_ON_PAGE):PRODUCTS_ON_PAGE+((page-1) * PRODUCTS_ON_PAGE)]

#     else:
#         products = Product.objects.all()[0+((page-1) * PRODUCTS_ON_PAGE):PRODUCTS_ON_PAGE+((page-1) * PRODUCTS_ON_PAGE)]

#     return JsonResponse({
#         "products": [
#             {
#                 "id": product.id,
#                 "image": product.get_image_url(),
#                 "title": product.title,
#                 "price": product.price,
#                 "tags": [
#                     {
#                         "title": tag.title,
#                         "color": tag.color
#                     }
#                     for tag in product.tags.all()
#                 ],
#                 "subcategory": product.subcategory.id
#             }
#             for product in products
#         ]
#     })


# def get_product_in_subcategory(request, uid):
#     subcategory = Subcategory.objects.get(id=uid)
#     products = Product.objects.all().filter(subcategory=subcategory)

#     return JsonResponse({
#         "products": [
#             {
#                 "id": product.id,
#                 "image": product.get_image_url(),
#                 "title": product.title,
#                 "price": product.price,
#                 "tags": [
#                     {
#                         "title": tag.title,
#                         "color": tag.color
#                     }
#                     for tag in product.tags.all()
#                 ],
#                 "subcategory": uid
#             } for product in products
#         ]
#     })
