$(document).ready(function() {
  $('.updatebutton').on('click', function(){


    var task_id = $(this).attr('task_id');


    req = $.ajax({
      url : '/check_task',
      type : 'POST',
      data : {id : task_id}
    });


    req.done(function(data) {
      $('#buttonimg' + task_id).attr('src', data.button_img);
      $('#content' + task_id).text(data.Content);
      if (data.Content == 'Completed'){
      $('#button' + task_id).attr('class', 'updatebutton btn btn-sm btn-outline-danger');
    }
    else {
      $('#button' + task_id).attr('class', 'updatebutton btn btn-sm btn-outline-success');
    }
     })


  });
});
