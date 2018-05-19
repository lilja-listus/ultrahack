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
          url: 'api/login',
          type: 'POST',
          data: loginStr, 
          dataType: 'json'
          });
        });
      });
    });
