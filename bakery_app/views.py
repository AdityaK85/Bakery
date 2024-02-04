from django.shortcuts import render
from .models import *
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_control
from Project_utilty.decorators import  handle_admin_page_exception
# Create your views here.


def login(request):
    return render(request , 'htmls/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def index(request , user):
    sales_obj = SalesMaster.objects.all().order_by("-id")
    sales_count = SalesMaster.objects.all().count()
    purchased_count = ItemsMaster.objects.all().count()
    sale_report_obj = []
    for i in sales_obj:
        sales_obj = SalesMaster.objects.get(id = i.id)
        for j in eval(i.item_list):
            get_item = SubCategory.objects.get(id = j["id"])
            category_exists = any(category['category'] == get_item.fk_category.category_name for category in sale_report_obj)
            if not category_exists:
                sale_report_obj.append({'category': get_item.fk_category.category_name, 'revenue': 0.0})

            for category in sale_report_obj:
                if category['category'] == get_item.fk_category.category_name:
                    item_tax = float(j["price"]) if get_item.fk_category.tax == 'Free' else  float(j["price"]) + (float(j["price"]) * int(get_item.fk_category.tax) / 100) 
                    category['revenue'] += item_tax
            
    total_revenue = sum(category['revenue'] for category in sale_report_obj)
    context = {'total_revenue': total_revenue , 'sales_count' : sales_count , 'purchased_count' : purchased_count }
    return render( request,  'htmls/dashboard.html' , context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def CategoriesItem(request , user):
    cat_obj = Category.objects.all().order_by('-id')
    string = render_to_string('render_to_String/r_t_s_categoryItem.html', {'category_obj': cat_obj})
    context = {'string': string} 
    return render( request,  'htmls/add_new_item.html', context )



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def viewCategory(request , user,  id):
	cat_obj = SubCategory.objects.filter(fk_category_id = id).order_by('-id')
	cat_name = Category.objects.get(id = id)
	string = render_to_string('render_to_String/r_t_s_viewCategory.html', {'category_obj': cat_obj})
	context = {'string': string , 'cat_name':cat_name}  
	return render( request,'htmls/viewCategory.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def Sales(request, user):
    cat_obj = Category.objects.all().order_by('-id')
    return render( request,  'htmls/add_sales.html' , {'cat_obj':cat_obj} )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def itemDetails(request ,user,  id):
    if SalesMaster.objects.filter(id = id).exists():
        item_obj = SalesMaster.objects.get(id = id)
        item_details = []
        total_price = 0.0
        for j in eval(item_obj.item_list):
            get_item = SubCategory.objects.get(id = j["id"])
            item_details.append({
                'id': get_item.id,
                'item_image': get_item.sub_category_img, 
                'item_name': get_item.sub_category_name, 
                'item_tax': get_item.fk_category.tax, 
                'quantity': j["qty"]  ,
                'price': float(j["price"]) if get_item.fk_category.tax == 'Free' else  float(j["price"]) + (float(j["price"]) * int(get_item.fk_category.tax) / 100) ,
                'main_price': j["main_price"]
            })

            tax_cal_amt = float(j["price"]) if get_item.fk_category.tax == 'Free' else  float(j["price"]) + (float(j["price"]) * int(get_item.fk_category.tax) / 100)
            total_price += tax_cal_amt
        context = {'item_obj': item_obj, 'item_details': item_details , 'total_price': total_price}
    return render(request , 'htmls/item_details.html' , context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def Purchase(request , user):
    purchase_obj = ItemsMaster.objects.all().order_by("-id")
    rendered = render_to_string('render_to_string/r_t_s_purchase.html' , {'purchase_obj': purchase_obj})
    context = { 'rendered' : rendered }
    return render(request , 'htmls/add_purchase.html' , context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def RecivedOrders(request , user):
    sale_obj = SalesMaster.objects.all().order_by('-id')
    rendered = render_to_string('render_to_string/r_t_s_recivedOrder.html' , {'sale_obj' : sale_obj})
    context = { 'rendered' : rendered }
    return render( request,  'htmls/recived_order.html' ,  context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def live_invoice(request,user ,  id):
    if SalesMaster.objects.filter(id = id).exists():
        item_obj = SalesMaster.objects.get(id = id)
        item_details = []
        total_price = 0.0
        for j in eval(item_obj.item_list):
            get_item = SubCategory.objects.get(id = j["id"])
            item_details.append({
                'id': get_item.id,
                'item_image': get_item.sub_category_img, 
                'item_name': get_item.sub_category_name, 
                'item_tax': get_item.fk_category.tax, 
                'quantity': j["qty"]  ,
                'price': float(j["price"]) if get_item.fk_category.tax == 'Free' else  float(j["price"]) + (float(j["price"]) * int(get_item.fk_category.tax) / 100) ,
                'main_price': j["main_price"]
            })

            tax_cal_amt = float(j["price"]) if get_item.fk_category.tax == 'Free' else  float(j["price"]) + (float(j["price"]) * int(get_item.fk_category.tax) / 100)
            total_price += tax_cal_amt
        context = {'item_obj': item_obj, 'item_details': item_details , 'total_price': total_price}
    return render(request , 'htmls/invoice.html' , context)


def send_link(request):
    return render(request , 'htmls/send_link.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def Expenses(request , user):
    exp_obj = Expense.objects.all().order_by("-id")
    rendered = render_to_string('render_to_string/r_t_s_expenses.html' , {'exp_obj' : exp_obj})
    context = { 'rendered' : rendered }
    return render(request , 'htmls/expenses.html' , context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def sale_reports(request ,user):
    sales_obj = SalesMaster.objects.all().order_by("-id")
    sale_report_obj = []
    for i in sales_obj:
        sales_obj = SalesMaster.objects.get(id = i.id)
        for j in eval(i.item_list):
            get_item = SubCategory.objects.get(id = j["id"])
            category_exists = any(category['category'] == get_item.fk_category.category_name for category in sale_report_obj)
            if not category_exists:
                sale_report_obj.append({'category': get_item.fk_category.category_name, 'revenue': 0.0})

            for category in sale_report_obj:
                if category['category'] == get_item.fk_category.category_name:
                    item_tax = float(j["price"]) if get_item.fk_category.tax == 'Free' else  float(j["price"]) + (float(j["price"]) * int(get_item.fk_category.tax) / 100) 
                    category['revenue'] += item_tax
            
    total_revenue = sum(category['revenue'] for category in sale_report_obj)
    rendered = render_to_string('render_to_string/r_t_s_sale_report.html' , {'sale_report_obj' : sale_report_obj , 'total_revenue':total_revenue})
    context = { 'rendered' : rendered }
    return render(request , 'htmls/sale_reports.html' , context)




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@handle_admin_page_exception
def account(request , user):
    user_obj = UserDetails.objects.get(id = user.id)
    return render(request , 'htmls/account.html', {'user_obj':user_obj})