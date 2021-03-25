from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import os

SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)

class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self, *args, **kwargs):
        return self.category

class Product(models.Model):
    product = models.CharField(verbose_name='Product Name', max_length=255)
    slug = models.CharField(null=True, editable=False, max_length=255)
    price = models.FloatField()
    category = models.ManyToManyField(Category, related_name='product')
    is_featured = models.BooleanField(default=False)

    def __str__(self, *args, **kwargs):
        return self.product

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product)
        return super(Product, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    product_carts = instance.product_cart.filter(checked_out=False)
    if product_carts.exists():
        for product_cart in product_carts:
            product_cart.save()
            
class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='media/', height_field='height', width_field='width')

    def __str__(self):
        return f'{self.product.slug}-{self.width}x{self.height}'

@receiver(models.signals.post_delete, sender=Gallery)
def auto_delete_gallery_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Gallery)
def auto_delete_gallery_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class ProductCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='product_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    qty = models.PositiveSmallIntegerField(verbose_name='Quantity', default=1)
    size = models.CharField(choices=SIZE_CHOICES, max_length=1)
    checked_out = models.BooleanField(default=False)
    total = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self, *args, **kwargs):
        return f'{self.product} {self.size} {self.qty}'
    
    def save(self, *args, **kwargs):
        self.total = int(self.product.price) * int(self.qty)
        return super(ProductCart, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=ProductCart)
def product_cart_post_save(sender, instance, created, **kwargs):
    if instance.checked_out == False:
        carts = instance.cart.filter(checked_out=False)
        if carts.exists():
            for cart in carts:
                cart.save()

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='cart')
    products = models.ManyToManyField(ProductCart, related_name='cart')
    checked_out = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self, *args, **kwargs):
        return f'{self.user} {self.total}'

    def save(self, *args, **kwargs):
        return super(Cart, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=Cart)
def cart_post_save(sender, instance, created, **kwargs):
    cart_total = 0
    for product in instance.products.all():
        cart_total += product.total

    if not cart_total == instance.total:
        instance.total = cart_total
        instance.save()
