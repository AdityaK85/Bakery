import {log, callAjax, sweetAlertMsg, showToastMsg} from '../CommonJS/common.js';

// $("#users_list").addClass("mm-active");

$(document).ready(function () {
    $(document).bind("keypress", function (e) {
      if (e.keyCode == 13) {
        $("#btn_login").trigger("click");
      }
    });
});



window.Login_Admin = async function() {
    document.getElementById('btn_login').disabled = true;

    var username = $('#username').val();
    var password = $('#admin_password').val();


    if (username == "") {

        showToastMsg("Username", "Please enter username", 'error');
        $('#username').focus()
        document.getElementById('btn_login').disabled = false;
    }
    else if (password == "") {
        
        showToastMsg("Password", "Please enter password", 'error');
        $('#password').focus()
        document.getElementById('btn_login').disabled = false;
    }
    else {

        var data = {

            'username': username,
            'password': password,
        }

        var response = await callAjax('/admin_login_aj/',data );

        if (response.status == 1)
        {
            document.getElementById('btn_login').disabled = false;
            window.location.href = "/Dasboard/" 
        }
        else if (response.status == 0)
        {
            document.getElementById('btn_login').disabled = false;
            showToastMsg("Error", response.msg, 'error')
        }
        else{

            document.getElementById('btn_login').disabled = false;
            showToastMsg("Error", 'Something Went Wrong', 'error')
        }
    }
  }
