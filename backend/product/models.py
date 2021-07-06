from rest_framework.exceptions import ValidationError as RESTValidationError
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models import Sum
import os
import random

SIZE_CHOICES = (
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
)

IMAGE_TYPE_CHOICES = (
    ('O', 'Other'),
    ('PF', 'Product Front'),
    ('PB', 'Product Back'),
    ('M', 'With Model(s)'),
)

RATING_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self, *args, **kwargs):
        return self.name

class Product(models.Model):
    name = models.CharField(verbose_name='Product Name', max_length=255)
    slug = models.CharField(null=True, editable=False, max_length=255, unique=True)
    description = models.CharField(null=True, blank=True, max_length=1024)
    price = models.FloatField(null=True, blank=True, default=0)
    category = models.ManyToManyField(Category, related_name='product')
    material = models.TextField(null=True, blank=True, max_length=255, default='')
    is_featured = models.BooleanField(null=True, blank=True, default=False)
    rating = models.FloatField(null=True, blank=True, default=0)

    def __str__(self, *args, **kwargs):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.description: self.description = 'This product does not have a description yet.'
        return super(Product, self).save(*args, **kwargs)

@receiver(models.signals.post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    product_carts = instance.product_cart.filter(checked_out=False)
    if product_carts.exists():
        for product_cart in product_carts:
            product_cart.save()

@receiver(models.signals.pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
    check_slug = Product.objects.filter(slug=instance.slug)
    if check_slug and instance not in check_slug:
        instance.slug = f"{instance.slug}-{random.randint(0, 100000)}"
            
class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery')
    image_type = models.TextField(choices=IMAGE_TYPE_CHOICES, default=IMAGE_TYPE_CHOICES[0][0], max_length=2)
    height = models.IntegerField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to='', height_field='height', width_field='width')

    def __str__(self):
        return f'{self.image_type}-{self.product.slug}-{self.width}x{self.height}'

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

class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='review')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.CharField(null=True, blank=True, max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Rating on {self.product.name}"

@receiver(models.signals.post_save, sender=Review)
@receiver(models.signals.post_delete, sender=Review)
def set_product_rating_ps(sender, instance, **kwargs):
    all_reviews = Review.objects.filter(product=instance.product)
    review_count = all_reviews.count()
    review_sum = all_reviews.aggregate(Sum('rating'))

    product = Product.objects.get(id=instance.product.id)
    product.rating = review_sum['rating__sum'] / review_count if review_count else 0
    product.save()

@receiver(models.signals.pre_save, sender=Review)
def review_pre_save(sender, instance, **kwargs):
    review = Review.objects.filter(user=instance.user, product=instance.product)
    
    if review and instance not in review:
        raise RESTValidationError('This user already reviewed this product', code=409)

    if not instance.rating:
        instance.rating = 0
    
    if instance.rating > 5 or instance.rating < 1:
        raise RESTValidationError('Rating should be between 1-5', code=400)
