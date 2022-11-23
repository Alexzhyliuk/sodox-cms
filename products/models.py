from django.db import models
from django.conf import settings


class Application(models.Model):
    
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=64)
    message = models.TextField()

    def __str__(self):
        return str(self.name) + ": " + str(self.message[:20]) + "..."


class Tag(models.Model):

    title = models.CharField(max_length=20)
    color = models.CharField(max_length=7)

    def __str__(self):
        return str(self.title)


class Manufacturer(models.Model):

    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to='manufacturers/')
    inactive_image = models.ImageField(upload_to="manufacturers/inactive/")

    def __str__(self):
        return str(self.title)


class Overcategory(models.Model):

    title = models.CharField(max_length=128)
    manufacturer = models.ForeignKey(Manufacturer, related_name='overcategories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.manufacturer.title}: {self.title}"


class Category(models.Model):

    title = models.CharField(max_length=64)
    manufacturer = models.ForeignKey(Manufacturer, related_name='categories', on_delete=models.CASCADE)
    overcategory = models.ForeignKey(Overcategory, related_name='categories', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.overcategory:
            return f"{self.manufacturer.title}: {self.title} | Сверхкатегория: {self.overcategory.title}"
        else:
            return f"{self.manufacturer.title}: {self.title}"


    def save(self, *args, **kwargs):
        if self.overcategory:
            if self.overcategory.manufacturer == self.manufacturer:
                return super().save(*args, **kwargs)
            return "Категория и сверхкатегория должны относиться к одному производителю"
        else:
            return super().save(*args, **kwargs)


class Subcategory(models.Model):

    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}: {self.category.title}: {self.category.manufacturer.title}"


class Product(models.Model):

    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.CharField(max_length=200)
    description = models.TextField()
    image_choice = models.FilePathField(path=settings.IMAGE_PATH, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    marks = models.TextField(blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, related_name='products', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, related_name='products', on_delete=models.CASCADE)

    var1 = models.CharField(max_length=64, null=True, blank=True)
    var2 = models.CharField(max_length=64, null=True, blank=True)
    var3 = models.CharField(max_length=64, null=True, blank=True)
    var4 = models.CharField(max_length=64, null=True, blank=True)
    var5 = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return str(self.title) + ": " + str(self.price)

    def save(self, *args, **kwargs):
        if self.subcategory.category.manufacturer == self.manufacturer:
            return super().save(*args, **kwargs)
        return "Подкатегория должна относиться к этому же производителю"

    def get_image_url(self):
        if self.image_choice:
            path = str(self.image_choice)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''

    def get_vars_count(self):
        return int(bool(self.var1)) + int(bool(self.var2)) +int(bool(self.var3)) +int(bool(self.var4)) + int(bool(self.var5))

    def get_vars(self):
        vars = [self.var1, self.var2, self.var3, self.var4, self.var5]
        active_vars = []
        for var in vars:
            if var:
                active_vars.append(var)

        return active_vars


class ProductCharacteristic(models.Model):

    product = models.ForeignKey(Product, related_name='characteristic', on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=300)

    var1 = models.CharField(max_length=100, null=True, blank=True)
    var2 = models.CharField(max_length=100, null=True, blank=True)
    var3 = models.CharField(max_length=100, null=True, blank=True)
    var4 = models.CharField(max_length=100, null=True, blank=True)
    var5 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.code}: {self.product.title}"

class ProductImage(models.Model):

    title = models.CharField(max_length=100)
    image = models.FilePathField(path=settings.IMAGES_PATH)
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title) + " : " + str(self.product.title)

    def get_image_url(self):
        if self.image:
            path = str(self.image)
            path = path.split(f"{settings.BASE_DIR}")[1]
            return path
        return ''


class ProductOrder(models.Model):

    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=64)
    message = models.TextField()
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.title}: {self.phone}"


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

