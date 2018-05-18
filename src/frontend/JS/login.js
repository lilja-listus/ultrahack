$(document).ready(function() {

$("#submitButton").click(function(){
  $.ajax({
    type: 'POST', 
    url: 'http://localhost:5000/api/login', 
    dataType: 'json',
    data: {'login': login, 'password': password},
    success: function (x) {                
      $("#add_err").html(x.response);

      //to check whether the login was successful
       $('#loginForm').hide();
            $('div#loginResult').text("data.success: " + data.success );
            $('div#loginResult').addClass("success");
    },
    beforeSend:function(){
      $("#add_err").html("Loading...")
    }
  });
  return false;
});

});