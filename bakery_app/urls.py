from django.urls import path
from .views import *
from .views_aj import *
from django.conf import settings
from django.conf.urls.static import static

admin_urls = [
    path('', login),
    path('Dasboard/', index),
    path('Categories/', CategoriesItem),
    path('Sales/', Sales),
    path('Purchase/', Purchase),
    path('RecivedOrders/', RecivedOrders),
    path('send_link/', send_link),
    path('Expenses/', Expenses),
    path('invoice/<int:id>', live_invoice),
    path('viewCategory/<int:id>', viewCategory),
    path('itemDetails/<int:id>', itemDetails),
]


ajax_urls = [
    path('admin_login_aj/', admin_login_aj),
    path('logout_admin/', logout_admin),
    path('add_services_aj/', add_services_aj),
    path('delete_category_aj/', delete_category_aj),
    path('add_item_aj/', add_item_aj),
    path('delete_item_aj/', delete_item_aj),
    path('change_category/', change_category),
    path('add_sale_aj/', add_sale_aj),
    path('add_puchase_aj/', add_puchase_aj),
    path('delete_item_aj/', delete_item_aj),
    path('make_payment_aj/', make_payment_aj),
    path('change_order_status_aj/', change_order_status_aj),
    path('send_invoice_to_email/', send_invoice_to_email),
    path('add_expense_aj/', add_expense_aj),
    path('delete_exp_aj/', delete_exp_aj),
    path('cod_payment_aj/', cod_payment_aj),
    path('sale_reports/', sale_reports),
    path('get_report_aj/', get_report_aj),
    path('get_filter_report_aj/', get_filter_report_aj),
    path('account/', account),
    path('view_password/', view_password),
    path('change_password/', change_password),
]


urlpatterns = [ *admin_urls, *ajax_urls] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)