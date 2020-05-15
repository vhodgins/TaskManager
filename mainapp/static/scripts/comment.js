$(document).ready(function(){

  $('.comment-form').submit(function(event) {
    event.preventDefault();
    event.stopImmediatePropagation();
    var id = $(this).attr('task_id');
    console.log(id);
    var comment_content = document.getElementById("comment").value;


    req = $.ajax({
      url : '/make_comment',
      type : 'POST',
      data : {content : comment_content, post : id}
    });


    req.done(function(data) {
        window.location.reload()
    })


  })
})
