$(document).ready(function() {

  //Check / Uncheck Script

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
  });


  });

  var timer = 0;


  $('.upvotebutton').on('click', function(event){
    event.preventDefault();


  //  var state = $(this).attr('state');

    var task_id = $(this).attr('task_id');

    $('#like'+task_id).attr('style', 'color: green; font-weight: bold; margin-top:3px; font-size:10pt;')

    if ((($('#upvote'+task_id).attr('value') === "1")) && (timer==0)){
      timer =1;


      req = $.ajax({
        url : '/upvote',
        type : 'POST',
        data : {id : task_id, lean: 'neutral'}
      });
      req.done(function(data) {
        timer = 0;
        $('#downvote'+task_id).attr('value', "0");
        $('#upvote'+task_id).attr('value', "0");
        $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
        $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; color:black;');
        $('#like'+task_id).attr('style', 'color:black; font-size:10pt;')
        $('#like'+task_id).text(data.likes);
      });
    }

    else if (timer==0) {

      timer = 1;

      req = $.ajax({
        url : '/upvote',
        type : 'POST',
        data : {id : task_id, lean: 'pos'}
      });
      req.done(function(data) {
        timer = 0;
        $('#downvote'+task_id).attr('value', "0");
        $('#upvote'+task_id).attr('value', "1");
        $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
        $('#upvote'+task_id).attr('style', 'background-color:green; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
        $('#like'+task_id).text(data.likes);
      });
    }
    });




  $('.downvotebutton').on('click', function(event){
        event.preventDefault();

        var task_id = $(this).attr('task_id');

        $('#like'+task_id).attr('style', 'color: red;  font-weight: bold; margin-top:3px; font-size:10pt;')

        if ((($('#downvote'+task_id).attr('value') === "-1")) && (timer ==0)) {
          timer = 1;

          req = $.ajax({
            url : '/upvote',
            type : 'POST',
            data : {id : task_id, lean: 'neutral'}
          });
          req.done(function(data) {
            timer = 0;
            $('#downvote'+task_id).attr('value', "0");
            $('#upvote'+task_id).attr('value', "0");
            $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
            $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; ');
            $('#like'+task_id).attr('style', 'color:black; font-size:10pt;')
              $('#like'+task_id).text(data.likes);
          });


        }
        else if (timer==0){
          timer =1;

        req = $.ajax({
          url : '/upvote',
          type : 'POST',
          data : {id : task_id, lean: 'neg'}
        });
        req.done(function(data) {
          timer = 0;
          $('#downvote'+task_id).attr('value', "-1");
          $('#upvote'+task_id).attr('value', "0");
          $('#downvote'+task_id).attr('style', 'background-color:red; height:20px; width:20px; border-radius:50%; text-decoration:none;');
          $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; ');
          $('#like'+task_id).text(data.likes);
        });


        }






  });
  });
// Upvote Scripts
