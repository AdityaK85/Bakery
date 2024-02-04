import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';

$("#item_sidebar").addClass("active");
$("#category_tbl").DataTable();




window.add_category = async function() {

    var type = $('#dropdown').val();
    var category_name = $('#category_name').val();
    var tax = $('#customInput').val();
    var category_id = $('#category_id').val();

    var flag = 'update' ;
    if (category_id.trim() == "" ) {
        flag = 'add'
    }

    if (category_name.trim() === "") {

        showToastMsg("Alert", "Please enter your category name.", 'error');
        $('#category_name').focus()
    }

    else if (type === "custom_tax" && tax.trim() === "") {
            showToastMsg("Alert", "Please enter tax", 'error');
            $('#customInput').focus()
    }
   
    else {

        var data = {
            'category_name':category_name,
            'tax':tax,
            'type':type,
            'flag':flag ,
            'category_id':category_id
        }

        var response = await callAjax('/add_services_aj/', data );

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




window.OpenUpdateModel = function(id, category_name , tax) {
    $('#backDropModalTitle').html('Update Category');
    $('#model_save_btn').html('Update');
    $('#category_name').val(category_name);
    $('#category_id').val(id);
    var selectElement = document.getElementById("dropdown");
    if (tax != 'Free') {
        
        for (var i = 0; i < selectElement.options.length; i++) {
            if (selectElement.options[i].value === "custom_tax") {
              selectElement.options[i].selected = true;
            }
          }
         $('#customInput').val(tax);
         document.getElementById("customInput").style.display = 'block'
        
    }else{
        for (var i = 0; i < selectElement.options.length; i++) {
            if (selectElement.options[i].value === "Free") {
              selectElement.options[i].selected = true;
            }
          }
         document.getElementById("customInput").style.display = 'none'
    }

    var modal = new bootstrap.Modal(document.getElementById('backDropModal'));
    modal.show();


    modal._element.addEventListener('hidden.bs.modal', function () {
        $('#category_name').val('');
        $('#model_save_btn').html('Save');
        $('#backDropModalTitle').html('Add New Category');
        $('#category_id').val('');
        document.getElementById("customInput").style.display = 'none'
        selectElement.selectedIndex = 0;
    });
}




  window.delete_service = async function(cat_id)
{
 
    var preference = await sweetAlertMsg('Delete Category', "Do you want to delete this Category?", 'question', 'cancel', 'Yes', )
   
    var data = {
        'cat_id': cat_id,
    }

    if (preference)
    {
        
        var response = await callAjax('/delete_category_aj/', data );
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



