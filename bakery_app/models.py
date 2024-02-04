from django.db import models

# Create your models here.


class UserDetails(models.Model):
    username = models.CharField(max_length=100, null=True,blank=True)
    password = models.CharField(max_length=100, null=True,blank=True)


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True,blank=True)
    tax = models.CharField(max_length=100, null=True,blank=True)
    

class SubCategory(models.Model):
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    sub_category_name = models.CharField(max_length=100, null=True,blank=True)
    sub_category_img = models.FileField(upload_to='SubCategory_Img/', null=True,blank=True)
    price = models.FloatField( null=True,blank=True)
    qty = models.IntegerField( null=True,blank=True)
    

class SalesMaster(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('SUCCESS', 'SUCCESS'),
        ('CANCLED', 'CANCLED')
    )
    order_id = models.CharField(max_length=100, null=True,blank=True)
    name = models.CharField(max_length=100, null=True,blank=True)
    email = models.CharField(max_length=100, null=True,blank=True)
    phone = models.CharField(max_length=100, null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    item_list = models.TextField( null=True,blank=True)
    order_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=100, choices = STATUS ,  default = 'PENDING', null=True,blank=True)
    created_dt = models.DateTimeField(null=True,blank=True)



class ItemsMaster(models.Model):
    measurement = (
        ('Kilogram', 'Kilogram'),
        ('Gram', 'Gram'),
        ('Milligram', 'Milligram'),
        ('Liter', 'Liter'),
        ('Milliliter', 'Milliliter'),
    )
    purchase_dt = models.DateField(null=True,blank=True)
    element = models.CharField( max_length=100, null=True,blank=True)
    qty = models.CharField(max_length=100,  null=True,blank=True)
    unit_price = models.CharField(max_length=100,  null=True,blank=True)
    price = models.CharField(max_length=100,  null=True,blank=True)
    unit_of_measurement = models.CharField(max_length=100, choices = measurement , null=True,blank=True)
    note = models.TextField( null=True,blank=True)
    created_dt = models.DateTimeField(null=True,blank=True)



class Expense(models.Model):
    category = models.CharField( max_length=100, null=True,blank=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    receipt_image = models.ImageField(upload_to='expense_receipts/', null=True, blank=True)
    created_dt = models.DateTimeField(null=True,blank=True)