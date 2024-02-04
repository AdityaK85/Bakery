import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

$("#sales_sidebar").addClass("active");




window.ChangeCategory = async function(value){
    window.change_item_id = []
    var response = await callAjax('/change_category/', {'id': value} );
    if (response.status == '1') {
        console.log(response.render)
        if (response.render != 'None') {
            $("#render_item").html(response.render)
            change_item_id.push(response.item_id)
        } 
        else {
            $("#render_item").html('<center> <h6>Select the Item</h6> </center>')
        }
    }
}


window.changePrice = function( qty , id , price ){

    var total_price = price * qty
    $(`#sale_price_${id}`).val(total_price)

}



window.add_sale = async function(item_list) {

    var customer_fullname = $('#customer_fullname').val();
    var customer_phone = $('#customer_phone').val();
    var customer_email = $('#customer_email').val();
    var customer_address = $('#customer_address').val();
    var order_date = $('#order_date').val();
    var emailfilter = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i;

    if (customer_fullname.trim() === "") {

        showToastMsg("Full Name", "Please enter customer fullname", 'error');
        $('#customer_fullname').focus()
    }
    else if (customer_phone.trim() === "") {

        showToastMsg("Phone", "Please enter customer phone", 'error');
        $('#customer_phone').focus()
    }
    else if (customer_email.trim() === "") {

        showToastMsg("Email", "Please enter email address", 'error');
        $('#customer_email').focus()
    }
    else if ( !emailfilter.test(customer_email) && customer_email.trim() != "") {

        showToastMsg("Invalid Email", "Please enter a valid email", 'error');
        $('#customer_email').focus()
    }
  
    else if (customer_address.trim() === "") {

        showToastMsg("Address", "Please enter customer address", 'error');
        $('#customer_address').focus()
    }
    else if (order_date === "") {

        showToastMsg("Order Date", "Please enter order date when you want", 'error');
        $('#order_date').focus()
    }
    else if (item_list.length <= 0) {
        showToastMsg("No Items", "Please select the items ", 'error');

    }
    else {

        var data = {
            'customer_fullname':customer_fullname,
            'customer_phone':customer_phone,
            'customer_email':customer_email,
            'customer_address':customer_address,
            'order_date':order_date,
            'item_list':item_list.map(item => Object.values(item)[0])
        }
        var response = await callAjax('/add_sale_aj/', JSON.stringify(data));

        if (response.status == 1)
        {
            showToastMsg('Sucess',response.msg, 'success'); 
            location.href = `/itemDetails/${response.id}`
            
        }
        else if (response.status == 0)
        {
            
            showToastMsg("Error", response.msg, 'error')
        }
        else{
            showToastMsg("Error", 'Something Went Wrong...', 'error')
        }
    }
  }