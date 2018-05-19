$(function() {

$("#submitButton").click(function(){
  
   var email = $("#email").val();
   var password = $("#password").val();
       

   var login = new Object();
       login.email = email;
       login.password =  password;

       var loginStr = JSON.stringify(login); 
       alert(loginStr); 

   $(function sendData() {
          $.ajax({
          url: 'http://ec2-34-230-45-89.compute-1.amazonaws.com/api/login',
          type: 'POST',
          data: loginStr, 
          dataType: 'json'
          });
        });


       });
    });
