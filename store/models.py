from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# module for user for address in profile
class Address(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    mobile = models.CharField(max_length=150, null=True, verbose_name="mobile")
    locality = models.CharField(max_length=150, verbose_name="Nearest Location")
    city = models.CharField(max_length=150, verbose_name="City")
    state = models.CharField(max_length=150, verbose_name="State")

    def __str__(self):
        return self.locality

# Restaurnat
class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Category Title")
    slug = models.SlugField(max_length=55, verbose_name="Category Slug")
    description = models.TextField(blank=True, verbose_name="Category Description")
    category_image = models.ImageField(upload_to='category', blank=True, null=True, verbose_name="Category Image")
    owner = models.CharField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    addres = models.CharField(max_length=10000, null=True, blank=True)
    area = models.CharField(max_length=1000, null=True, blank=True)
    opentime = models.TimeField(null=True, blank=True)
    closestime = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title

# menu
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Product Title")
    slug = models.SlugField(max_length=160, verbose_name="Product Slug")
    product_image = models.ImageField(upload_to='product', blank=True, null=True, verbose_name="Product Image")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # which restaurant
    category = models.ForeignKey(Category, verbose_name="Product Categoy", on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Is Active?")
    is_featured = models.BooleanField(verbose_name="Is Featured?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_at', )

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    def __str__(self):
        return str(self.user)
    
    # Creating Model Property to calculate Quantity x Price
    @property
    def total_price(self):
        return self.quantity * self.product.price


STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled')
)

class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name="Shipping Address", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")
    ordered_date = models.DateTimeField(auto_now_add=True, verbose_name="Ordered Date")
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=50,
        default="Pending"
        )
