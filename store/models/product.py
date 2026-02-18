from django.db import models
from .category import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    
    # Specifications
    brand = models.CharField(max_length=50, default='', null=True, blank=True)
    ram = models.CharField(max_length=50, default='', null=True, blank=True)
    storage = models.CharField(max_length=50, default='', null=True, blank=True)
    camera = models.CharField(max_length=100, default='', null=True, blank=True)
    battery = models.CharField(max_length=50, default='', null=True, blank=True)
    screen_size = models.CharField(max_length=50, default='', null=True, blank=True)
    color = models.CharField(max_length=50, default='', null=True, blank=True)

    # Variant Linking
    variant_name = models.CharField(max_length=100, default='', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='variants')

    # Bundle Linking
    compatible_accessories = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='main_products')
    
    # Dynamic Specifications
    specifications = models.JSONField(default=dict, blank=True, null=True)

    def get_bundle_price(self):
        total = self.price
        for acc in self.compatible_accessories.all():
            total += acc.price
        return total

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products();