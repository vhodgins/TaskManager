$(document).ready(function(){

  $('#searchbar').submit(function(e){
    q = 'http://localhost:5000/search/' + $('#searchfield').val();
    document.location.href = q ;
    e.preventDefault();

  });



})
