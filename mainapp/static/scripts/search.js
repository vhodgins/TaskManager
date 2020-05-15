$(document).ready(function(){

  $('#searchbar').submit(function(e){
    if ($('#searchfield').val() != '') {
    q = 'http://localhost:5000/search/' + $('#searchfield').val();
    document.location.href = q ;
    e.preventDefault();
  }

  });

  $('.followbtn').on('click', function(e){

    id = $(this).attr('userid');
    if ($(this).html() == 'Follow') {
      $(this).html('Unfollow');
    }
    else {
      $(this).html('Follow')
    }


    req = $.ajax({
      url : '/add_friend',
      type : 'POST',
      data : {id : id}
    });

    req.done(function() {

    })

    e.preventDefault();

  })

})
