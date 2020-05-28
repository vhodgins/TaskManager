




  function homelist() {
    a = $('#list-select').val();
    $('.mainpagelist:visible').hide();
    $('#accountposts' + a).show(250);
    console.log(a);


  }
