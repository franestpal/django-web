from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify
from django.db.models.signals import pre_save
import string
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

# Create your models here.
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image
from django.utils.text import slugify
from django.db.models.signals import pre_save
import string
from django.db import models

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
 
ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

CATEGORY_CHOICES = (
    ('P', 'Pescados'),
    ('M', 'Mariscos'),
    ('C', 'Conservas')
)

LABEL_CHOICES = (
    ('S', 'sale'),
    ('N', 'new'),
    ('P', 'promotion')
)

class Slide(models.Model):
    caption1 = models.CharField(max_length=100)
    caption2 = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    image = models.ImageField(help_text="Size: 1920x570")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {}".format(self.caption1, self.caption2)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:category", kwargs={
            'slug': self.slug
        })


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product/{item.title}", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("product/{item.title}/add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("product/{item.title}/remove-from-cart", kwargs={
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
         if not self.discount_price:
              self.discount_price = ""   
         super(Item, self).save(*args, **kwargs)


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name = 'order_item_user_store', on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'order_user', on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        'BillingAddress', related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'BillingAddress', related_name='billing_address', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        'Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    '''
    1. Item added to cart
    2. Adding a BillingAddress
    (Failed Checkout)
    3. Payment
    4. Being delivered
    5. Received
    6. Refunds
    '''

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name = 'billing_user', on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = 'billing_user_store',
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Refund(models.Model):
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.pk}"

def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename



@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        # print("Se acaba de crear un usuario y su perfil enlazado")



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")


    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.name






class Post(models.Model):
    Post_name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True, default = None)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    image = models.ImageField(verbose_name="Imagen", upload_to="blog", null=True, blank=True)

    def __str__(self):
        return self.Post_name

    def get_absolute_url(self):
        return reverse("store:product", kwargs={'pk': self.pk})

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={"pk": self.pk})

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
         if not self.discount_price:
              self.discount_price = None    
         super(Post, self).save(*args, **kwargs)



class OrderItem(models.Model):
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.Post.Post_name}'


class Order(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    stock_no = models.CharField(max_length=10)
    description_short = models.CharField(max_length=50)
    description_long = models.TextField()
    image = models.ImageField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("store:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("store:remove-from-cart", kwargs={
            'slug': self.slug
        })