from django import forms

from products.models import Product


class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('title', 'price', 'short_description', 'description', 'image_choice', 'subcategory', 'manufacturer', 'var1', 'var2', 'var3', 'var4', 'var5')