from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(UserDetails)
class AdminUserAdmin(admin.ModelAdmin):
    list_display=['id','username','password']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name','tax']

@admin.register(SubCategory)
class Sub_CategoryAdmin(admin.ModelAdmin):
    list_display=['id','fk_category','sub_category_name','price','qty']

@admin.register(SalesMaster)
class SalesMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'name', 'phone', 'email', 'address', 'status', 'item_list']

@admin.register(ItemsMaster)
class ItemsMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase_dt', 'element', 'qty', 'unit_price', 'price', 'unit_of_measurement']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'description', 'amount', 'date', 'receipt_image', 'created_dt']