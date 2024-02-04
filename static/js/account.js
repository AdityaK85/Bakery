import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

$("#account_sidebar").addClass("active");


window.viewPassword = async function()
{
    var view_pwd = $("#view_pwd").val()
    if (view_pwd.trim() == "") {
        showToastMsg("Password", "Please enter password", 'error');
        $('#view_pwd').focus()
    } 
    else {
        
        var data = {
            'view_pwd' : view_pwd
        }
        var response = await callAjax('/view_password/', data );
        if (response.status == 1) {
            $("#view_password").html(response.pwd)
            $(".btn-close").trigger('click')
        }
        else if (response.status == 0){
            showToastMsg("Invalid Password", "!Enter password is invalid", 'error');
        }
        
        else {
            showToastMsg("Error", "Something went wrong", 'error');
        }  
    }
}



window.changePassword = async function()
{
    var change_username = $("#change_username").val()
    var current_pwd = $("#current_pwd").val()
    var change_pwd = $("#change_pwd").val()

    if (current_pwd.trim() == "") {
        showToastMsg("Password", "Please enter current password", 'error');
        $('#current_pwd').focus()
    } 
    else {
        
        var data = {
            'change_username' : change_username,
            'current_pwd' : current_pwd,
            'change_pwd' : change_pwd
        }
        var response = await callAjax('/change_password/', data );
        if (response.status == 1) {

            showToastMsg("Success", response.msg, 'success');
            await new Promise(resolve => setTimeout(resolve, 1500)); 
            location.reload();
        }
        else if (response.status == 0){
            showToastMsg("Invalid Password", response.msg, 'error');
        }
        
        else {
            showToastMsg("Error", "Something went wrong", 'error');
        }  
    }
}
