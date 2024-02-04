import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

$("#sale_report_sidebar").addClass("active");
$("#sale_rep_a").addClass("active")



var current_dt = new Date();
var Today_dt = current_dt.toISOString().split('T')[0];
$('#from_dt').attr('max', Today_dt);

$('#from_dt').change(function()
{
    var from_date = $("#from_dt").val();
    $('#to_dt').attr('min',from_date)
});

// $('#to_dt').attr('max', Today_dt);

$('#to_dt').change(function()
{
    var to_date = $("#to_dt").val();
    $('#from_dt').attr('max',to_date)
});


window.getReports = async function(ele , type) {
    if (type == "purchased") {
        $("#pur_rep_a").addClass("active")
        $("#sale_rep_a").removeClass("active")
        $("#exp_rep_a").removeClass("active")
    }
    else if (type == "expenses") {
        $("#pur_rep_a").removeClass("active")
        $("#sale_rep_a").removeClass("active")
        $("#exp_rep_a").addClass("active")
    }
    else if (type == "sales") {
        $("#pur_rep_a").removeClass("active")
        $("#sale_rep_a").addClass("active")
        $("#exp_rep_a").removeClass("active")
    }
    var response = await callAjax('/get_report_aj/', {'type':type});
    if (response.status == 1) {
        var capitalizedType = response.type.charAt(0).toUpperCase() + response.type.slice(1);
        $("#report_div").html(response.rendered)
        $("#braudcamb, #card_rep_title").html(capitalizedType);
        $("#check_report").val(response.type)
    }
    else {
        showToastMsg("Error", 'Something Went Wrong...', 'error')
    }
}



window.filterData = async function() {
    var type = $("#check_report").val()
    var from_dt = $("#from_dt").val()
    var to_dt = $("#to_dt").val()

    if (from_dt != '' &&  to_dt == '') {
        showToastMsg("Error", "Please enter To date.", 'error');
        $("#to_dt").focus()
    } 
    else if (from_dt == '' &&  to_dt != '') {
        showToastMsg("Error", "Please enter From date.", 'error');
        $('#from_dt').focus()
    }
    else {
        
        var data = {
            'type':type,
            'from_dt':from_dt,
            'to_dt':to_dt,
        }
        var response = await callAjax('/get_filter_report_aj/', data);
        if (response.status == 1) {
            $("#report_div").html(response.rendered)
        }
        else {
            showToastMsg("Error", 'Something Went Wrong...', 'error')
        }   
    }
}


