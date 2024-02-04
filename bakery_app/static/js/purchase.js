import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

$("#purchase_sidebar").addClass("active");
$("#purchase_order_tbl").DataTable();

window.add_purchased = async function() {

    var purchase_dt = $('#purchase_dt').val();
    var element_name = $('#element_name').val();
    var qty = $('#qty').val();
    var measurement = $('#measurement').val();
    var unit_price = $('#unit_price').val();
    var total_price = $('#total_price').val();
    var note = $('#note').val();
    
    
    if (purchase_dt.trim() === "") {

        showToastMsg("Purchase Date", "Please enter purchase date.", 'error');
        $('#purchase_dt').focus()
    }
    else if (element_name.trim() === "") {

        showToastMsg("Element Name", "Please enter element name", 'error');
        $('#element_name').focus()
    }
    else if (qty.trim() === "") {

        showToastMsg("Quantity", "Please enter Quantity", 'error');
        $('#qty').focus()
    }
    else if (measurement.trim() === "") {

        showToastMsg("Measurement", "Please select measurement", 'error');
        $('#measurement').focus()
    }
    else if (unit_price.trim() === "") {

        showToastMsg("Unit Price", "Please enter Unit Price", 'error');
        $('#unit_price').focus()
    }
    else if (total_price.trim() === "") {

        showToastMsg("Total Price", "Please enter Total Price", 'error');
        $('#total_price').focus()
    }
    else {

        var data = {
            'purchase_dt':purchase_dt,
            'element_name': element_name,
            'qty': qty,
            'measurement': measurement,
            'unit_price': unit_price,
            'total_price': total_price,
            'note': note,
        }

        var response = await callAjax('/add_puchase_aj/',data );

        if (response.status == 1)
        {
            showToastMsg('Sucess',response.msg, 'success'); 
            await new Promise(resolve => setTimeout(resolve, 1500)); 
            location.reload();
            
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



window.viewPurchased = function(purchase_dt , name, qty , measurement , unit_price , Price , note ) {

    $("#element_name_model").html(name)
    $("#purchase_dt_model").html(purchase_dt)
    $("#note_model").html(note)
    $("#qty_model").html(qty)
    $("#measure_model").html(measurement)
    $("#unit_price_model").html(unit_price+'/-')
    $("#total_price_model").html(Price+'/-')

    var modalToggle = new bootstrap.Modal(document.getElementById('modalToggle'));
    modalToggle.show();
}




window.delete_item = async function(id)
{   
    var preference = await sweetAlertMsg(`Delete Item`, `Do you want to delete this Item?`, 'question', 'cancel', 'Yes', )
    var data = {
        'id': id,
    }
    if (preference)
    {
        var response = await callAjax('/delete_item_aj/', data );
        if (response.status == 1)
        {
            showToastMsg('Success',response.msg, 'success'); 
            await new Promise(resolve => setTimeout(resolve, 1500)); 
            location.reload();
        }
        else 
        {
            showToastMsg("Error", response.msg, 'error');
        }
    } 
}