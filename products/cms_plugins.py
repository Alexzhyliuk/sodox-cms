from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import gettext_lazy as _

from products.cms_models import Service, Task, Customer, Company, Hero, ContactIcon, Faq, CatalogImg


class ServicePlugin(CMSPluginBase):
	model = Service
	render_template = 'plugins/service.html'
	cache = False


class TasksPlugin(CMSPluginBase):
	model = Task
	render_template = 'plugins/task.html'
	cache = False


class CustomersPlugin(CMSPluginBase):
	model = Customer
	render_template = 'plugins/customer.html'
	cache = False


class CompanyPlugin(CMSPluginBase):
	model = Company
	render_template = 'plugins/company.html'
	cache = False


class HeroPlugin(CMSPluginBase):
	model = Hero
	render_template = 'plugins/hero.html'
	cache = False


class CatalogImgPlugin(CMSPluginBase):
	model = CatalogImg
	render_template = 'plugins/products_img.html'
	cache = False


class ContactIconPlugin(CMSPluginBase):
	model = ContactIcon
	render_template = 'plugins/contact_icon.html'
	cache = False


class FaqPlugin(CMSPluginBase):
	model = Faq
	render_template = 'plugins/faq.html'
	cache = False


plugin_pool.register_plugin(ServicePlugin)
plugin_pool.register_plugin(TasksPlugin)
plugin_pool.register_plugin(CustomersPlugin)
plugin_pool.register_plugin(CompanyPlugin)
plugin_pool.register_plugin(HeroPlugin)
plugin_pool.register_plugin(ContactIconPlugin)
plugin_pool.register_plugin(FaqPlugin)
plugin_pool.register_plugin(CatalogImgPlugin)




