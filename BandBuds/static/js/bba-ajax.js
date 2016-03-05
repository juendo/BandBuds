$('#going-button').click(function(){
    var goingid;
    goingid = $(this).attr("data-goingid");
    $.get('/bba/gig_attending/', {gig_id: goingid}, function(data){
               $('#going').html(data);
               $('#going-button').hide();
    });
});