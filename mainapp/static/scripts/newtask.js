$(document).ready(function(){

$('#newtask').submit(function(e){
  title = $('#titlearea').val();
  if ($('#List').val()) {
    list = $('#List').val();
  }
  else {
    list = id
  }
  date = $('#date').val();
  private = $('#private').val();
  console.log(date);




  req = $.ajax({
    url : '/newpost',
    type : 'POST',
    data : {title : title,
            list : list,
            date : date,
            private : private}
  })

  req.done(function(data){
    console.log('success');
      location.reload();
  })

  e.preventDefault();

})



})
