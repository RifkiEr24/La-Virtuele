from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.utils import IntegrityError
from product.models import Product, SIZE_CHOICES

class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='cart')
    checked_out = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self, *args, **kwargs):
        return f'{self.user}-{self.id}-{self.total}'

    def save(self, *args, **kwargs):
        return super(Cart, self).save(*args, **kwargs)

    def update_total(self, product_list):
        total = 0
        for product in product_list:
            total += product.subtotal
        self.total = total

        return self.save()

    def toggle_checkout(self):
        self.checked_out = not self.checked_out

        return self.save()

@receiver(models.signals.pre_save, sender=Cart)
def cart_pre_save(sender, instance, **kwargs):
    # There can only be one active (uncheckedout) cart
    try:
        cart = Cart.objects.filter(user=instance.user, checked_out=False)
        if cart.count() > 1: raise IntegrityError('This user already have an active cart')
    except Cart.DoesNotExist:
        pass

@receiver(models.signals.post_save, sender=Cart)
def cart_post_save(sender, instance, created, **kwargs):
    # Create a new cart for each product that are not selected during checkout
    if instance.checked_out and not created:
        unselected_product = [product.id for product in instance.product_cart.all() if not product.selected]
            
        if unselected_product:
            new_cart = Cart.objects.create(user=instance.user, checked_out=False)
        
        for product in unselected_product:
            product.cart = new_cart
            product.save()

class ProductCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='product_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_cart')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='product_cart', null=True, blank=True)
    qty = models.PositiveSmallIntegerField(verbose_name='Quantity', default=1)
    size = models.CharField(choices=SIZE_CHOICES, max_length=1)
    selected = models.BooleanField(default=False)
    subtotal = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self, *args, **kwargs):
        return f'{self.product} {self.size} {self.qty}'
    
    def save(self, *args, **kwargs):
        self.subtotal = int(self.product.price) * int(self.qty)
        return super(ProductCart, self).save(*args, **kwargs)

@receiver(models.signals.pre_save, sender=ProductCart)
def product_cart_pre_save(sender, instance, **kwargs):
    Cart.objects.get_or_create(user=instance.user, checked_out=False)

@receiver(models.signals.post_save, sender=ProductCart)
def product_cart_post_save(sender, instance, created, **kwargs):
    # Automatically assign a created product cart to user's active cart
    if created:
        instance.cart = Cart.objects.get(user=instance.user, checked_out=False)
        instance.save()

    # Update cart total
    instance.cart.update_total(ProductCart.objects.filter(cart=instance.cart, selected=True))

@receiver(models.signals.post_delete, sender=ProductCart)
def product_cart_post_delete(sender, instance, **kwargs):
    instance.cart.update_total(ProductCart.objects.filter(cart=instance.cart, selected=True))

class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='transaction')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='transaction')
    order_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=255)
    
    def __str__(self):
        return f'{self.user.username}-{self.order_id}'
