$(document).ready(function() {
  $('#newpost').on('click', function(event){
    event.preventDefault();


    var title = $('#newposttext').val();
    if (title) {


    req = $.ajax({
      url : '/processnewtask',
      type : 'POST',
      data : {title : title}
    });


    req.done(function(data) {
      console.log(data.name);
      $("#accountposts").prepend(`
        <li class="mainpagelist">
        <div class="card ml-5 bg-light mb-4" id="tasksection${data.id}"style="width:85%; height:80px">
          <div class="card-body" style="margin-left: -30px; margin-top:-7px;">
            <p class="text-muted ml-5 float-right" style="font-size:10pt; margin-top: 5px;">${data.date}</p>

            <div class="row ml-2" style="margin-top: -5px;">
              <img src="${data.userimg}" class="ml-4" style="border: 2px solid lightgrey; border-radius:10%; width:40px; height: 40px;" alt="">
           <h5 class="ml-1 mt-1"><a style="color:inherit; text-decoration:none;"href="${data.accountpage}">${data.name}</a></h5>
              </div>
            <div class="row">

            <ul style="list-style-type:none; display:flex; flex-direction: row;">
              <li class="font-weight-normal"><a href="${data.postpage}" style="color:inherit; text-decoration:none;">${data.title}</a></li>
              <li class="font-weight-light ml-3" id="content${data.id}"></li>

            </ul>
            <span style="position:absolute;right: 20px;">
              <form class="" action="index.html" method="post">


            <a href="#" class="updatebutton " id="button${data.id}" style="background: transparent;
          border: none !important; margin-top:-20px;"  task_id="${data.id}" name="button">
              <img style="width:30px; margin-top:-10px;" id="buttonimg${data.id}" src="${data.check}">
            </a>





              </form>
            </span>
          </div>


          </div>
        </div>
        </li>
`);






    });

   }
  });
});
