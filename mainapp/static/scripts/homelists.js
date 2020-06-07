




  function homelist() {
    a = $('#list-select').val();
    $('.mainpagelist:visible').hide();
    $('#accountposts' + a).slideDown  (250);
    console.log(a);


  }
