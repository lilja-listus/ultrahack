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
       //alert(JSON.stringify(trip));

              //sending data to the server  
       $(function sendData() {
          $.ajax({
          url: 'http://ec2-34-230-45-89.compute-1.amazonaws.com/api/new_travel_notice',
          type: 'POST',
          //data: myString,
          data: myString, 
          dataType: 'json'
          });
        });
    });
});

