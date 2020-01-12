$(document).ready(function() {


$('.upvotebutton').on('click', function(event){
  event.preventDefault();


//  var state = $(this).attr('state');

  var task_id = $(this).attr('task_id');

  $('#like'+task_id).attr('style', 'color: green; font-weight: bold; margin-top:3px; font-size:10pt;')

  if (($('#upvote'+task_id).attr('value') === "1")){

    req = $.ajax({
      url : '/upvote',
      type : 'POST',
      data : {id : task_id, lean: 'neutral'}
    });
    req.done(function(data) {
      $('#downvote'+task_id).attr('value', "0");
      $('#upvote'+task_id).attr('value', "0");
      $('#downvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none;');
        $('#upvote'+task_id).attr('style', 'background-color:green; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
        $('#like'+task_id).text(data.likes);
    });
  }

  else {
    req = $.ajax({
      url : '/upvote',
      type : 'POST',
      data : {id : task_id, lean: 'pos'}
    });
    req.done(function(data) {
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

      if (($('#downvote'+task_id).attr('value') === "-1")) {

        req = $.ajax({
          url : '/upvote',
          type : 'POST',
          data : {id : task_id, lean: 'neutral'}
        });
        req.done(function(data) {
          $('#downvote'+task_id).attr('value', "0");
          $('#upvote'+task_id).attr('value', "0");
          $('#downvote'+task_id).attr('style', 'background-color:red; height:20px; width:20px; border-radius:50%; text-decoration:none;');
            $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
            $('#like'+task_id).text(data.likes);
        });


      }
      else{
      req = $.ajax({
        url : '/upvote',
        type : 'POST',
        data : {id : task_id, lean: 'neg'}
      });
      req.done(function(data) {
        $('#downvote'+task_id).attr('value', "-1");
        $('#upvote'+task_id).attr('value', "0");
        $('#downvote'+task_id).attr('style', 'background-color:red; height:20px; width:20px; border-radius:50%; text-decoration:none;');
          $('#upvote'+task_id).attr('style', 'background-color:white; height:20px; width:20px; border-radius:50%; text-decoration:none; color:green;');
          $('#like'+task_id).text(data.likes);
      });


      }


);





});
