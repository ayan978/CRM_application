from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.id} {self.name}'

class Product(models.Model):
    Category = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
        ('Delivery', 'Delivered'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=Category)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.id} {self.name}'


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    def __str__(self): 
        return f'{self.customer.name} {self.product.name}'




    
    

