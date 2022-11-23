from cms.wizards.wizard_base import Wizard
from cms.wizards.wizard_pool import wizard_pool

from products.forms import ProductWizardForm


class ProductWizard(Wizard):
	pass

product_wizard = ProductWizard(
	title="Product",
	weight=200,
	form=ProductWizardForm,
	description="Create a new Product"
	)

wizard_pool.register(product_wizard)