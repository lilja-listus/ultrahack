//date picker
$(function() {
    
    $( "#datepickerStart" ).datepicker();
    //.css("background-color", "blue");;
    $( "#datepickerEnd" ).datepicker();
  });
 
    
$(function() {
    $("#buttonFind").click(function(){
       var destination = $("#destination").val();
       var startDate =$("#datepickerStart").val().toString();
       
       //JS date object
       var dateStart = new Date(startDate);
       var endDate = $("#datepickerEnd").val().toString();
       var dateEnd = new Date(endDate);
       dateEnd = dateEnd.getTime();
       dateStart = dateStart.getTime();
      
 //creating new Json object for passing
       var trip = new Object();
       trip.destination = destination;
       trip.start = dateStart;
       trip.end = dateEnd;
       var myString = JSON.stringify(trip);

              //sending data to the server  
       $(function sendData() {
          $.ajax({
          url: 'http://ec2-34-230-45-89.compute-1.amazonaws.com/api/new_travel_notice',
          type: 'POST',
          data: myString, 
          dataType: 'json'
          });
        });
    });
});

//parsing json to create autocomplete for search
$.ajax({
  url: 'http://ec2-34-230-45-89.compute-1.amazonaws.com/api/sharing_targets',
}).done(function(data) {

var arrayUsers = [];

for (var i = 0; i<data.users.length; i++){
  arrayUsers[i] = data.users[i].name;

}
$("#search").autocomplete({
source:arrayUsers})               
})

.fail(function() {
  alert("Ajax failed to fetch data")
});

