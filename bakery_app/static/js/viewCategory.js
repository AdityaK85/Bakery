import { log, callAjax, sweetAlertMsg, showToastMsg } from '../CommonJS/common.js';
$("#item_sidebar").addClass("active");

window.select_image = async function (input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            var imageElement = document.getElementById("displayed_image");
            var selected_image = document.getElementById("selected_image");

            var img = new Image();
            img.src = e.target.result;

            img.onload = function () {
                if (img.width === 100 && img.height === 100) {
                    if (imageElement) {
                        imageElement.src = e.target.result;
                        selected_image.src = e.target.result;
                    }
                } else {
                    
                    showToastMsg("Service Image", "Please select only 100x100 px images.", 'error');
                    input.value = "";
                }
            };
        };

        reader.readAsDataURL(input.files[0]);
    }
}



window.add_item = async function() {
    var flag = 'update'
    var item_id = $('#item_id').val();
    if ( item_id.trim() === ''){
        flag = 'add'
    }
    var item_name = $('#item_name').val();
    var fk_cat_id = $('#fk_cat_id').val();
    var item_rate = $('#item_rate').val();
    var item_stock = $('#item_stock').val();
    var thambnail = document.getElementById("selected_image");
    var files = thambnail.files[0];
    
    
    if (item_name.trim() === "") {

        showToastMsg("Service Name", "Please enter your Item name.", 'error');
        $('#item_name').focus()
    }
    else if (item_rate.trim() === "") {

        showToastMsg("Rate", "Please enter rate", 'error');
        $('#item_rate').focus()
    }
    else if (item_stock.trim() === "") {

        showToastMsg("Stock", "Please enter Available Stock", 'error');
        $('#item_stock').focus()
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
        data.append("flag", flag);
        data.append("item_name", item_name);
        data.append("item_stock", item_stock);
        data.append("item_rate", item_rate);
        data.append("fk_cat_id", fk_cat_id);
        data.append("item_id", item_id);

        var response = await callAjax('/add_item_aj/',data ,  null, null, null, true);

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

window.updateItemCollaps = function( id, item_name, item_rate, item_stock, item_img ) {
    $("#collapseExample").addClass('show')
    var collapsibleElement = document.getElementById("collapseExample");
    $('#item_id').val(id);
    $('#item_name').val(item_name);
    $('#item_rate').val(item_rate);
    $('#item_stock').val(item_stock);
    $("#displayed_image").attr('src', item_img);

    collapsibleElement.addEventListener("hidden.bs.collapse", function () {
        $('#item_id').val('');
        $('#item_name').val('');
        $('#item_rate').val('');
        $('#item_stock').val('');
        $("#displayed_image").attr('src', '/static/assets/img/elements/1.jpg');
      });
}



  window.delete_item = async function(item_id)
{
 
    var preference = await sweetAlertMsg('Delete Item', "Do you want to delete this Item?", 'question', 'cancel', 'Yes', )
   
    var data = {
        'item_id': item_id,
    }

    if (preference)
    {
        
        var response = await callAjax('/delete_item_aj/', data );
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



window.closeCollaps = function(){
    $('#item_id').val('');
    $('#item_name').val('');
    $('#item_rate').val('');
    $('#item_stock').val('');
    $("#displayed_image").attr('src', '/static/assets/img/elements/1.jpg');
    $('#collapseExample').removeClass('show');
}   