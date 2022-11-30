from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic.detail import DetailView
from products.models import *
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import QuerySet
import math
import csv
from django.conf import settings
from products.csv_upload import upload_csv

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


@upload_csv(custom={"success": "Производители", "title": "производителей"})
def add_manufacturers(request, row=[]):

    Manufacturer.objects.get_or_create(
            title=row[1]['title'],
            image=settings.MANUFACTURER_IMAGE_PATH + str(row[1]['image']),
            inactive_image=settings.MANUFACTURER_IMAGE_PATH + str(row[1]['inactive_image']),
        )


@upload_csv(custom={"success": "Категории", "title": "категории"})
def add_categories(request, row=[]):
   
    Category.objects.get_or_create(
            manufacturer = Manufacturer.objects.filter(title=str(row[1]['manufacturer'])).first(),
            title=row[1]['title'],
            image=settings.CATEGORY_IMAGE_PATH + str(row[1]['image']),
            short_description=row[1]["short_description"],
            description=row[1]["description"],
            advantages=row[1]["advantages"],
            recommendation=row[1]["recommendation"],
        )


@upload_csv(custom={"success": "Подкатегории", "title": "подкатегории"})
def add_subcategories(request, row=[]):

    Subcategory.objects.get_or_create(
            category = Category.objects.filter(title=str(row[1]['category']), manufacturer__title=str(row[1]["manufacturer"])).first(),
            title=row[1]['title'],
            image=settings.SUBCATEGORY_IMAGE_PATH + str(row[1]['image']),
            description=row[1]["description"],
            review=row[1]["review"],
        )


@upload_csv(custom={"success": "Номенклатуры", "title": "номенклатуры"})
def add_nomenclatures(request, row=[]):

    Nomenclature.objects.get_or_create(
            subcategory = Subcategory.objects.filter(title=str(row[1]['subcategory'])).filter(category__title=str(row[1]["category"])).filter(category__manufacturer__title=str(row[1]["manufacturer"])).first(),
            title=row[1]['title'],
            var1=row[1]['var1'] if str(row[1]['var1']) != 'nan' else '',
            var2=row[1]['var2'] if str(row[1]['var2']) != 'nan' else '',
            var3=row[1]['var3'] if str(row[1]['var3']) != 'nan' else '',
            var4=row[1]['var4'] if str(row[1]['var4']) != 'nan' else '',
            var5=row[1]['var5'] if str(row[1]['var5']) != 'nan' else '',
        )


@upload_csv(custom={"success": "Строки для номенклатур", "title": "строки для номенклатур"})
def add_nomenclatures_rows(request, row=[]):

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


@upload_csv(custom={"success": "Загрузки", "title": "загрузки"})
def add_downloads(request, row=[]):

    Downloads.objects.get_or_create(
            subcategory = Subcategory.objects.filter(title=str(row[1]['subcategory'])).filter(category__title=str(row[1]["category"])).filter(category__manufacturer__title=str(row[1]["manufacturer"])).first(),
            series=row[1]['series'],
            model=row[1]['model'],
            file=settings.DOWNLOADS_FILE_PATH + str(row[1]["file"]),
        )


class CreateApplication(View):
    def post(self, request, *args, **kwargs):

        new_application(request)
        
        return redirect(reverse("products:index"))
