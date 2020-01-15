$(document).ready(function() {

  $('.settings').on('click', function(event){
      var id = $(this).attr("task_id");
      var settings = document.createElement("a");
      settings.appendChild(document.createTextNode("Delete"));
      document.getElementById(id).appendChild(settings);
  })

});
