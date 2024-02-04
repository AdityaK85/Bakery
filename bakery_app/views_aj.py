import traceback
from django.http import JsonResponse
from django.shortcuts import redirect
from Project_utilty.Utility import Payment
from Project_utilty.decorators import get_date_label, handle_ajax_exception, is_admin_authenticated, is_authenticated
from Project_utilty.send_emails import send_html_email
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
import datetime
from datetime import datetime 
from django.db.models import Sum



@csrf_exempt
def admin_login_aj(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    if UserDetails.objects.filter(username = username , password = password).exists():
        admin_obj  = UserDetails.objects.get(username = username , password = password)
        request.session['admin_user_id'] = admin_obj.id
        request.session['admin_user_type'] = "admin"
        return JsonResponse({"status": 1, "msg": "Success"})
    else:
        return JsonResponse({"status": 0, "msg": "Invalid Credentials"})




@csrf_exempt
def logout_admin(request):
    try :
        if request.session.get("admin_user_id") :
            del request.session['admin_user_id']
            del request.session['admin_user_type']
    except :
        traceback.print_exc()
    return redirect('/')


@csrf_exempt
@handle_ajax_exception
def add_services_aj(request):
    msg = 'Invalid Data...'
    category_name = request.POST.get('category_name')
    tax = request.POST.get('tax')
    types = request.POST.get('type')
    id = request.POST.get('category_id')
    flag = request.POST.get('flag')
    if flag == "add":
        Category.objects.create(category_name=category_name, tax=types if types == 'Free' else tax)   
        msg = 'Category added Successfully.'
    else:
        obj = Category.objects.get(id=id)
        obj.category_name = category_name
        obj.tax = types if types == 'Free' else tax
        obj.save()
        msg = 'Category updated Successfully.'

    send_data = {'status':1, 'msg': msg}
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def add_item_aj(request):
    msg = 'Invalid Data...'
    item_name = request.POST.get('item_name')
    item_rate = float(request.POST.get('item_rate')) 
    item_stock = request.POST.get('item_stock')
    files = request.FILES.get('files')
    fk_cat_id = request.POST.get('fk_cat_id')
    id = request.POST.get('item_id')
    flag = request.POST.get('flag')
    if flag == "add":
        SubCategory.objects.create(fk_category_id =fk_cat_id, sub_category_name = item_name , sub_category_img=files, price=item_rate , qty = item_stock)   
        msg = 'Stock added Successfully.'
    else:
        obj = SubCategory.objects.get(id=id)
        obj.sub_category_name = item_name
        obj.sub_category_img = files
        obj.price = item_rate
        obj.qty = item_stock
        obj.save()
        msg = 'Stock updated Successfully.'

    send_data = {'status':1, 'msg': msg}
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def delete_category_aj(request):
    id = request.POST.get('cat_id')
    if Category.objects.filter(id = id).exists():
        Category.objects.get(id=id).delete()
        send_data = {'status':1, 'msg': 'Category deleted Successfully.'}
    else:
        send_data = {'status':0, 'msg': 'Something went Wrong.'}
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def delete_item_aj(request):
    id = request.POST.get('item_id')
    if SubCategory.objects.filter(id = id).exists():
        SubCategory.objects.get(id=id).delete()
        send_data = {'status':1, 'msg': 'Item deleted Successfully.'}
    else:
        send_data = {'status':0, 'msg': 'Something went Wrong.'}
    return JsonResponse(send_data)

@csrf_exempt
@handle_ajax_exception
def change_category(request):
    id = request.POST.get('id')
    render = 'None'
    item_id = []
    if id != "0":
        item_obj = SubCategory.objects.filter(fk_category_id = id)
        item_id = SubCategory.objects.filter(fk_category_id=id).values_list('id', flat=True)
        render = render_to_string('render_to_string/r_t_s_item_list.html', {'item_obj':item_obj})
    context = {'status':1, 'msg':'data fetched' , 'render':render , 'item_id': list(item_id) if item_id else [] } 
    return JsonResponse(context , safe=False)

import json
import random

@csrf_exempt
@handle_ajax_exception
def add_sale_aj(request):
    data = json.loads(request.body.decode('utf-8'))
    customer_fullname = data.get('customer_fullname')
    customer_phone = data.get('customer_phone')
    customer_email = data.get('customer_email')
    customer_address = data.get('customer_address')
    order_date = data.get('order_date')
    item_list = data.get('item_list')
    sales_obj =  SalesMaster.objects.create( order_id = random.randint(100000, 999999),  name= customer_fullname, phone = customer_phone, email = customer_email , address = customer_address , item_list = item_list , order_date = order_date , created_dt = datetime.now()  ,status = 'PENDING')
    send_data = {'status':1, 'msg':'Sales Added' , 'id' : sales_obj.id }
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def add_puchase_aj(request):
    purchase_dt = request.POST.get('purchase_dt')
    element_name = request.POST.get('element_name')
    qty = request.POST.get('qty')
    measurement = request.POST.get('measurement')
    total_price = request.POST.get('total_price')
    unit_price = request.POST.get('unit_price')
    note = request.POST.get('note')
    ItemsMaster.objects.create(purchase_dt = purchase_dt, element = element_name, qty = qty , unit_of_measurement = measurement , unit_price = unit_price , price = total_price, note = note , created_dt = datetime.now())
    send_data = {'status':1, 'msg':'Purchase data added in system' }
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def delete_item_aj(request):
    id = request.POST.get('id')
    ItemsMaster.objects.filter(id = id).delete()
    send_data = {'status':1, 'msg':'Item Delete Successfully' }
    return JsonResponse(send_data)



@csrf_exempt
@handle_ajax_exception
def make_payment_aj(request):
    id = request.POST.get('id')
    amt = request.POST.get('amt')
    type = request.POST.get('type')
    amount = round((float(amt)))    
    amount = amount * 100
    REDIRECT_URL = f'http://127.0.0.1:8000/invoice/{id}'
    sales_obj = SalesMaster.objects.get(id = id)
    response = Payment(amount, REDIRECT_URL , REDIRECT_URL, '9876543210' )
    if response[0] == False:
        return JsonResponse({'stutus':"0","msg":response[1]})
    else:
        response = json.loads(response[1])
        phonepe_redirecturl = response['data']["instrumentResponse"]["redirectInfo"]["url"] 
    if type == 'send_link':
        context = {'link':phonepe_redirecturl , 'username' : sales_obj.name  }
        subject = f"Purchased Invoice {sales_obj.order_id} "
        dummy_str = render_to_string('htmls/send_link.html', context)
        to_email = sales_obj.email
        send_html_email(subject, dummy_str, to_email)

    send_data = {'status':1, 'msg':'Payment Successed' , 'phonepe_redirecturl': phonepe_redirecturl , 'type' :type }
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def change_order_status_aj(request):
    id = request.POST.get('id')
    if SalesMaster.objects.filter(id = id).exists():
        sales_obj = SalesMaster.objects.get(id = id)
        sales_obj.status = 'SUCCESS'
        sales_obj.save()
        item_details = []
        total_price = 0.0
        for j in eval(sales_obj.item_list):
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
        context = {'item_obj': sales_obj, 'item_details': item_details , 'total_price': total_price}
        if sales_obj.email:
            subject = "Login OTP"
            dummy_str = render_to_string('htmls/invoice.html', context)
            to_email = sales_obj.email
            send_html_email(subject, dummy_str, to_email)
    send_data = {'status':1, 'msg':'Success' }
    return JsonResponse(send_data)



@csrf_exempt
@handle_ajax_exception
def send_invoice_to_email(request):
    id = request.POST.get('id')
    if SalesMaster.objects.filter(id = id).exists():
        sales_obj = SalesMaster.objects.get(id = id)
        item_details = []
        total_price = 0.0
        for j in eval(sales_obj.item_list):
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
        context = {'item_obj': sales_obj, 'item_details': item_details , 'total_price': total_price}
        if sales_obj.email:
            subject = f"Purchased Invoice {sales_obj.order_id} "
            dummy_str = render_to_string('htmls/invoice.html', context)
            to_email = sales_obj.email
            send_html_email(subject, dummy_str, to_email)
    send_data = {'status':1, 'msg':'Invoice aend to customer email address' }
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def add_expense_aj(request):
    category_name = request.POST.get('category_name')
    exp_amt = request.POST.get('exp_amt')
    exp_dt = request.POST.get('exp_dt')
    description = request.POST.get('description')
    files = request.FILES.get('files')
    Expense.objects.create(category = category_name , description = description, amount = exp_amt , date = exp_dt , receipt_image = files , created_dt = datetime.now())
    send_data = {'status':1, 'msg':'Expenses added' }
    return JsonResponse(send_data)




@csrf_exempt
@handle_ajax_exception
def delete_exp_aj(request):
    item_id = request.POST.get('item_id')
    Expense.objects.filter(id = item_id).delete()
    send_data = {'status':1, 'msg':'Expense Data Delete Successfully' }
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def cod_payment_aj(request):
    id = request.POST.get('id')
    SalesMaster.objects.filter(id = id).update(status = 'SUCCESS')
    send_data = {'status':1, 'msg':'Order Status Will be Changed To Success' }
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def get_report_aj(request):
    type = request.POST.get('type')
    if type == "purchased":
        obj = ItemsMaster.objects.all().count()
        total_rev = ItemsMaster.objects.all().aggregate(total_rev=Sum('price'))
        context = {'obj': obj , 'total_rev' : total_rev['total_rev']}
        rendered = render_to_string('render_to_string/r_t_s_purchase_report.html', context)
    elif type == "expenses":
        obj = Expense.objects.all().count()
        total_rev = Expense.objects.all().aggregate(total_rev=Sum('amount'))
        context = {'obj': obj , 'total_rev' : total_rev['total_rev']}
        rendered = render_to_string('render_to_string/r_t_s_purchase_report.html', context)
    else :
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
    send_data = {'status':1, 'rendered':rendered , 'type':type}
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def get_filter_report_aj(request):
    type = request.POST.get('type')
    from_dt = request.POST.get('from_dt')
    to_dt = request.POST.get('to_dt')
    if type == "purchased":
        obj = ItemsMaster.objects.filter(created_dt__date__lte = to_dt, created_dt__date__gte = from_dt).count()
        total_rev = ItemsMaster.objects.filter(created_dt__date__lte = to_dt, created_dt__date__gte = from_dt).aggregate(total_rev=Sum('price'))
        context = {'obj': obj , 'total_rev' : total_rev['total_rev']}
        rendered = render_to_string('render_to_string/r_t_s_purchase_report.html', context)
    elif type == "expenses":
        obj = Expense.objects.filter(created_dt__date__lte = to_dt, created_dt__date__gte = from_dt).count()
        total_rev = Expense.objects.filter(created_dt__date__lte = to_dt, created_dt__date__gte = from_dt).aggregate(total_rev=Sum('amount'))
        context = {'obj': obj , 'total_rev' : total_rev['total_rev']}
        rendered = render_to_string('render_to_string/r_t_s_purchase_report.html', context)
    else :
        sales_obj = SalesMaster.objects.filter(created_dt__date__lte = to_dt, created_dt__date__gte = from_dt).order_by("-id")
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
    send_data = {'status':1, 'rendered':rendered , 'type':type}
    return JsonResponse(send_data)


@csrf_exempt
@handle_ajax_exception
def view_password(request):
    user_obj = is_admin_authenticated(request)
    view_pwd = request.POST.get('view_pwd')
    if UserDetails.objects.filter(id = user_obj.id).exists():
        user = UserDetails.objects.get(id = user_obj.id)
        if user.password == view_pwd:
            send_data = {'status':1 , 'pwd' : user.password}
        else:
            send_data = {'status':0 , 'pwd' : ''}
    return JsonResponse(send_data)



@csrf_exempt
def change_password(request):
    user_obj = is_admin_authenticated(request)
    change_username = request.POST.get("change_username")
    current_pwd = request.POST.get("current_pwd")
    change_pwd = request.POST.get("change_pwd")
    if UserDetails.objects.filter(id = user_obj.id).exists():
        user = UserDetails.objects.get(id = user_obj.id)
        if user.password == current_pwd:
            user.username = change_username if change_username != "" else user.username
            user.password = change_pwd if change_pwd != "" else user.password
            user.save()
            return JsonResponse({"status": 1, "msg": "Account Details Updated Successfully."})
        else:
            return JsonResponse({"status": 0, "msg": "The current password you entered is incorrect."})

