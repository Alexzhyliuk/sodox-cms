from django.db import models
from django.conf import settings


class Application(models.Model):
    
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=64)
    message = models.TextField()

    def __str__(self):
        return str(self.name) + ": " + str(self.message[:20]) + "..."

    class Meta:
        verbose_name_plural = "Заявки"


class Manufacturer(models.Model):

    title = models.CharField(max_length=64)
    image = models.FilePathField("Цветное изображение", path=settings.MANUFACTURER_IMAGE_PATH, blank=True, null=True)
    inactive_image = models.FilePathField("Бесцветное изображение", path=settings.MANUFACTURER_IMAGE_PATH, blank=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_image_url(self):
        if self.image:
            path = str(self.image)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''

    def get_inactive_image_url(self):
        if self.inactive_image:
            path = str(self.inactive_image)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''

    class Meta:
        verbose_name_plural = "Производители"
    


class Category(models.Model):

    manufacturer = models.ForeignKey(Manufacturer, related_name='categories', on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=64)
    image = models.FilePathField("Изображение", path=settings.CATEGORY_IMAGE_PATH, blank=True, null=True)
    short_description = models.CharField("Краткое описание", max_length=256)
    description = models.TextField("Описание")
    advantages = models.TextField("Преимущества")
    recommendation = models.TextField("Рекомендация")

    def __str__(self):
        return f"{self.manufacturer.title}: {self.title}"
    
    def get_image_url(self):
        if self.image:
            path = str(self.image)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''

    class Meta:
        verbose_name_plural = "Категории"


class Subcategory(models.Model):

    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=128)
    image = models.FilePathField("Изображение", path=settings.SUBCATEGORY_IMAGE_PATH, blank=True, null=True)
    description = models.TextField("Описание")
    review = models.TextField("Обзор")


    def __str__(self):
        return f"{self.title}: {self.category.title}: {self.category.manufacturer.title}"

    def get_image_url(self):
        if self.image:
            path = str(self.image)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''

    class Meta:
        verbose_name_plural = "Подкатегории"


class Nomenclature(models.Model):

    subcategory = models.OneToOneField(Subcategory, on_delete=models.CASCADE)
    title = models.CharField("Название", max_length=256)

    var1 = models.CharField(max_length=128, null=True, blank=True)
    var2 = models.CharField(max_length=128, null=True, blank=True)
    var3 = models.CharField(max_length=128, null=True, blank=True)
    var4 = models.CharField(max_length=128, null=True, blank=True)
    var5 = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    def get_vars_count(self):
        return int(bool(self.var1)) + int(bool(self.var2)) +int(bool(self.var3)) +int(bool(self.var4)) + int(bool(self.var5))

    def get_vars(self):
        vars = [self.var1, self.var2, self.var3, self.var4, self.var5]
        active_vars = []
        for var in vars:
            if var:
                active_vars.append(var)

        return active_vars

    class Meta:
        verbose_name_plural = "Номенклатура"


class NomenclatureRow(models.Model):

    nomenclature = models.ForeignKey(Nomenclature, related_name="rows", on_delete=models.CASCADE)
    model = models.CharField("Название", max_length=256)
    code = models.CharField("Код заказа", max_length=64)

    var1 = models.CharField(max_length=128, null=True, blank=True)
    var2 = models.CharField(max_length=128, null=True, blank=True)
    var3 = models.CharField(max_length=128, null=True, blank=True)
    var4 = models.CharField(max_length=128, null=True, blank=True)
    var5 = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.model}"

    class Meta:
        verbose_name_plural = "Строки номенклатуры"


class Downloads(models.Model):

    subcategory = models.ForeignKey(Subcategory, related_name="downloads", on_delete=models.CASCADE)
    series = models.CharField("Серии", max_length=256)
    model = models.CharField("Модель", max_length=256)
    file = models.FilePathField("Файл", path=settings.DOWNLOADS_FILE_PATH, blank=True, null=True)


    def __str__(self):
        return f"{self.model}"

    def get_file_url(self):
        if self.file:
            path = str(self.file)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''

    class Meta:
        verbose_name_plural = "Загрузки"





# class Product(models.Model):

#     title = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     short_description = models.CharField(max_length=200)
#     description = models.TextField()
#     image_choice = models.FilePathField(path=settings.IMAGE_PATH, blank=True, null=True)
#     tags = models.ManyToManyField(Tag, blank=True)
#     marks = models.TextField(blank=True, null=True)
#     subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
#     manufacturer = models.ForeignKey(Manufacturer, related_name='products', on_delete=models.CASCADE)

#     var1 = models.CharField(max_length=64, null=True, blank=True)
#     var2 = models.CharField(max_length=64, null=True, blank=True)
#     var3 = models.CharField(max_length=64, null=True, blank=True)
#     var4 = models.CharField(max_length=64, null=True, blank=True)
#     var5 = models.CharField(max_length=64, null=True, blank=True)

#     def __str__(self):
#         return str(self.title) + ": " + str(self.price)

#     def save(self, *args, **kwargs):
#         if self.subcategory.category.manufacturer == self.manufacturer:
#             return super().save(*args, **kwargs)
#         return "Подкатегория должна относиться к этому же производителю"

#     def get_image_url(self):
#         if self.image_choice:
#             path = str(self.image_choice)
#             path = path.split(f"{settings.BASE_DIR}")[1]
#             return path
#         return ''

#     def get_vars_count(self):
#         return int(bool(self.var1)) + int(bool(self.var2)) +int(bool(self.var3)) +int(bool(self.var4)) + int(bool(self.var5))

#     def get_vars(self):
#         vars = [self.var1, self.var2, self.var3, self.var4, self.var5]
#         active_vars = []
#         for var in vars:
#             if var:
#                 active_vars.append(var)

#         return active_vars


# class ProductCharacteristic(models.Model):

#     product = models.ForeignKey(Product, related_name='characteristic', on_delete=models.CASCADE)
#     model = models.CharField(max_length=100)
#     code = models.CharField(max_length=100)
#     description = models.CharField(max_length=300)

#     var1 = models.CharField(max_length=100, null=True, blank=True)
#     var2 = models.CharField(max_length=100, null=True, blank=True)
#     var3 = models.CharField(max_length=100, null=True, blank=True)
#     var4 = models.CharField(max_length=100, null=True, blank=True)
#     var5 = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return f"{self.code}: {self.product.title}"

# class ProductImage(models.Model):

#     title = models.CharField(max_length=100)
#     image = models.FilePathField(path=settings.IMAGES_PATH)
#     product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

#     def __str__(self):
#         return str(self.title) + " : " + str(self.product.title)

#     def get_image_url(self):
#         if self.image:
#             path = str(self.image)
#             path = path.split(f"{settings.BASE_DIR}")[1]
#             return path
#         return ''


# class ProductOrder(models.Model):

#     name = models.CharField(max_length=64)
#     phone = models.CharField(max_length=20)
#     email = models.CharField(max_length=64)
#     message = models.TextField()
#     product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.product.title}: {self.phone}"


class Coordinate(models.Model):

    title = models.CharField(max_length=100)
    coord_long = models.DecimalField(max_digits=25, decimal_places=20)
    coord_lat = models.DecimalField(max_digits=25, decimal_places=20)

    def __str__(self):
        return f"{self.title}"

    def get_coord(self):
        c_long = str(self.coord_long).split('.')
        c_lat = str(self.coord_lat).split('.')
        return [[int(c_long[0]), int(c_long[1])], [int(c_lat[0]), int(c_lat[1])]]

    class Meta:
        verbose_name_plural = "Координаты"