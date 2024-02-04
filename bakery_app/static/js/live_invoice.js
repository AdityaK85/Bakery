import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';


window.change_order_status = async function(id)
{   
    await callAjax('/change_order_status_aj/', { 'id': id } );
}

var id = $("#invoice_id").val()
change_order_status(id)