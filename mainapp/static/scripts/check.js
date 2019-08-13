$(document).ready(function() {


  $('.updatebutton').on('click', function(event){
    event.preventDefault();

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
      $('#button' + task_id).attr('class', 'updatebutton');
    }
    else {
      $('#button' + task_id).attr('class', 'updatebutton');
    }
     })


  });

  $('.upvotebutton').on('click', function(event){
    event.preventDefault();

    var task_id = $(this).attr('task_id');


    req = $.ajax({
      url : '/upvote',
      type : 'POST',
      data : {id : task_id, lean: 'hey'}
    });



    req.done(function(data) {

      $('#like'+task_id).text(data.likes)
    });

  });

  $('.downvotebutton').on('click', function(event){
    event.preventDefault();

    var task_id = $(this).attr('task_id');


    req = $.ajax({
      url : '/upvote',
      type : 'POST',
      data : {id : task_id, lean: ''}
    });



    req.done(function(data) {

      $('#like'+task_id).text(data.likes)
    });

  });


});
