$(document).ready(function(){

$('#newtask').submit(function(e){
  title = $('#titlearea').val();
  list = $('#List').val();
  date = $('#date').val();
  private = $('#private').val();
  console.log(date);
  
  e.preventDefault();

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
  })
  location.reload();
})



})
