import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

$("#expenses_sidebar").addClass("active");
$("#exp_tbl").DataTable();



window.add_expenses = async function() {
   
    var category_name = $('#category_name').val();
    var exp_dt = $('#exp_dt').val();
    var exp_amt = $('#exp_amt').val();
    var description = $('#description').val();
    var thambnail = document.getElementById("exp_recipt");
    var files = thambnail.files[0];
    
    
    if (category_name.trim() === "") {

        showToastMsg("Service Name", "Please enter your Item name.", 'error');
        $('#category_name').focus()
    }
    else if (exp_dt.trim() === "") {

        showToastMsg("Rate", "Please enter rate", 'error');
        $('#exp_dt').focus()
    }
    else if (exp_amt.trim() === "") {

        showToastMsg("Stock", "Please enter Available Stock", 'error');
        $('#exp_amt').focus()
    }
    else if (description.trim() === "") {

        showToastMsg("Description", "Please enter description", 'error');
        $('#description').focus()
    }
    else if (!files && thambnail.src == "") {

        showToastMsg("Image", "Please select Item image", 'error');
    }
    else if (files === undefined && thambnail.src == window.location.href) {

        showToastMsg("Image", "Please select Item image", 'error');
    }
    
   
    else {

        var data = new FormData();

        data.append("files", files);
        data.append("category_name", category_name);
        data.append("exp_amt", exp_amt);
        data.append("exp_dt", exp_dt);
        data.append("description", description);

        var response = await callAjax('/add_expense_aj/',data ,  null, null, null, true);

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



  window.delete_exp = async function(item_id)
  {
   
      var preference = await sweetAlertMsg('Delete Expense Data', "Do you want to delete this expense data?", 'question', 'cancel', 'Yes', )
     
      var data = {
          'item_id': item_id,
      }
  
      if (preference)
      {
          
          var response = await callAjax('/delete_exp_aj/', data );
          if (response.status == 1)
          {
              showToastMsg('Sucess',response.msg, 'success'); 
              await new Promise(resolve => setTimeout(resolve, 1500)); 
              location.reload();
          }
          else 
          {
              showToastMsg("Error", response.msg, 'error');
          }
      } 
  }
  