import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';


window.make_payment = async function(id , amt , type)
{   
    var data = {
        'id': id,
        'amt': amt,
        'type': type,
    }
    var response = await callAjax('/make_payment_aj/', data );
    if (response.status == 1)
    {
        if (response.type == 'send_link' ) {
            showToastMsg("Success", 'The payment link has been sent to the customer email.', 'success');
        }
        else {
            location.href = response.phonepe_redirecturl
        }
    }
    else 
    {
        showToastMsg("Error", response.msg, 'error');
    }
}

window.cod_payment = async function(id )
{   
    var data = {
        'id': id,
    }
    var response = await callAjax('/cod_payment_aj/', data );
    if (response.status == 1)
    {
        showToastMsg("Success", response.msg, 'success');
        await new Promise(resolve => setTimeout(resolve, 1500)); 
        location.reload();
    }
    else 
    {
        showToastMsg("Error", response.msg, 'error');
    }
}



window.send_invoice_to_email = async function(id)
{   
    var response = await callAjax('/send_invoice_to_email/', { 'id': id } );
    if (response.status == 1)
    {
        showToastMsg("Success", response.msg, 'success');
    }
    else 
    {
        showToastMsg("Error", response.msg, 'error');
    }
}