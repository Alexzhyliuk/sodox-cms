from django.db import models
from cms.models.pluginmodel import CMSPlugin


class Service(CMSPlugin):

    image = models.ImageField(upload_to="service/images")
    text = models.CharField(max_length=100)


class Task(CMSPlugin):

    number = models.IntegerField()
    text = models.CharField(max_length=300)


class Customer(CMSPlugin):

    image = models.ImageField(upload_to="customers/images/")


class Company(CMSPlugin):

    image = models.ImageField(upload_to="company/images/")
    title = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)


class Hero(CMSPlugin):

    image = models.ImageField(upload_to="hero/")


class CatalogImg(CMSPlugin):

    image = models.ImageField(upload_to='catalog/')


class ContactIcon(CMSPlugin):

    image = models.FileField(upload_to="contact_icons/images/")
    link = models.URLField(max_length=200, blank=True)


class Faq(CMSPlugin):

    title = models.CharField(max_length=100)
    text = models.CharField(max_length=500)


