$(document).ready(function() {

  var id = -1;




  $('.settings').on('click', function(event){

    if ($(this).attr("task_id")==id){
    $('.deletebutton').remove();
    $('.edit').remove();
    id = -1;
  }
  else{
    $('.deletebutton').remove();
    $('.edit').remove();
    id = -1;
      console.log('create');
      id = $(this).attr("task_id");
      var state = id;
      var settings = document.createElement("a");
      settings.innerHTML = "Delete";
      settings.id = (id + 'delete');
      settings.className = "deletebutton btn btn-sm btn-outline-danger";
      settings.style = 'position:absolute;  bottom:1px; left: 40px; ';
      settings.href = "#";
      var edit = document.createElement("a");
      edit.style = 'position:absolute;  bottom:1px; left: 105px; ';
      edit.innerHTML = 'Edit';
      edit.href = "posts/" + $(this).attr('t');
      edit.className = ("btn btn-sm btn-outline-info edit edit" + id);
      edit.id = (id + 'edit');
      document.getElementById(id).appendChild(settings);
      //document.getElementById(id).appendChild(edit);
    }
  }
  );

  $(document).on('click', '.deletebutton', function(event){
    var task_id =$(this).attr("id");
    req = $.ajax({
      url : '/delete_post',
      type : 'POST',
      data : {id : task_id}
    });


    req.done(function(data) {
      console.log(data.result);
      window.location.reload();
    });
  });


  /*$('.settings').on('click', function(event){
    if ($('.deletebutton')) {
    $('.deletebutton').remove();
  }

})*/


});
