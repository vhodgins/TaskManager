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
  //  var state = $(this).attr('state');

    var task_id = $(this).attr('task_id');

    if ((($('#upvote'+task_id).attr('value') === "0")) && (($('#downvote'+task_id).attr('value') === "-1"))){

      req = $.ajax({
        url : '/upvote',
        type : 'POST',
        data : {id : task_id, lean: 'up2'}
      });



      req.done(function(data) {
        $('#downvote'+task_id).attr('value', "0");
        $('#upvote'+task_id).attr('value', "1");
        $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
          $('#upvote'+task_id).attr('style', 'background-color:green; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
          $('#like'+task_id).text(data.likes);
      });


    }




    else if ($('#upvote'+task_id).attr('value') === "0") {
    req = $.ajax({
      url : '/upvote',
      type : 'POST',
      data : {id : task_id, lean: 'hey'}
    });



    req.done(function(data) {
      $('#downvote'+task_id).attr('value', "0");
      $('#upvote'+task_id).attr('value', "1");
      $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
        $('#upvote'+task_id).attr('style', 'background-color:green; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
        $('#like'+task_id).text(data.likes);
    });

}




  else if (($('#upvote'+task_id).attr('value') === "1")) {
        req = $.ajax({
          url : '/upvote',
          type : 'POST',
          data : {id : task_id, lean: ''}
        });



        req.done(function(data) {
          $('#downvote'+task_id).attr('value', "0");
          $('#upvote'+task_id).attr('value', "0");
          $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
            $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
            $('#like'+task_id).text(data.likes);
        });


  }




  });

  $('.downvotebutton').on('click', function(event){
        event.preventDefault();

        var task_id = $(this).attr('task_id');

        if ((($('#downvote'+task_id).attr('value') === "0")) && (($('#upvote'+task_id).attr('value') === "1"))){

          req = $.ajax({
            url : '/upvote',
            type : 'POST',
            data : {id : task_id, lean: 'down2'}
          });



          req.done(function(data) {
            $('#downvote'+task_id).attr('value', "-1");
            $('#upvote'+task_id).attr('value', "0");
            $('#downvote'+task_id).attr('style', 'background-color:red; height:20px; width:20px; border-radius:50%; text-decoration:none;');
              $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
              $('#like'+task_id).text(data.likes);
          });


        }


        else if ($('#downvote'+task_id).attr('value') === "0") {

            req = $.ajax({
              url : '/upvote',
              type : 'POST',
              data : {id : task_id, lean: ''}
            });




            req.done(function(data) {
              $('#downvote'+task_id).attr('value', "-1");
              $('#upvote'+task_id).attr('value', "0");
              $('#downvote'+task_id).attr('style', 'background-color:red; height:20px; width:20px; border-radius:50%; text-decoration:none; color:red;')
              $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;')
              $('#like'+task_id).text(data.likes)
            });
      }

      else if (($('#downvote'+task_id).attr('value') === "-1")) {
            req = $.ajax({
              url : '/upvote',
              type : 'POST',
              data : {id : task_id, lean: 'hey'}
            });



            req.done(function(data) {
              $('#downvote'+task_id).attr('value', "0");
              $('#upvote'+task_id).attr('value', "0");
              $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
                $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
                $('#like'+task_id).text(data.likes);
            });


      }




  });


});
