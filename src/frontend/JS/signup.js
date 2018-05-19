$(function() {
    $("#signupbtn").click(function(){

       var email = $("#email").val();
       var password = $("#password").val();
       var repeatPas = $("#repeatPass").val();
       var name = $("#name").val();
       var location = $("#location").val();



       //json object

       var newUser = new Object();
       newUser.email = email;
       newUser.password =  password;
       newUser.name = name;
       newUser.home = location;  

       var newUserStr = JSON.stringify(newUser); 

              //sending data to the server  
       $(function sendData() {
          $.ajax({
          url: 'http://ec2-34-230-45-89.compute-1.amazonaws.com/api/new_user',
          type: 'POST',
          //data: myString,
          data: newUserStr, 
          dataType: 'json',
          complete:
        function () {
            window.location = "/travel_notice.html";
        }
          });
        });

        



       });

    $("#cancelbtn").click(function(){
      window.location = "/login.html";
    });

    });




  