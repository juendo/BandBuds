$( document ).ready( function() {

		// scale calendar so cells retain circular proportion when window is resized.
	$( window ).resize(function(event) {
	    setCalendarHeight();
	});

	// when search button pressed, close filter panel and open search panel
	$( '#search-button' ).click( function() {
		$( '#search-panel' ).slideToggle(200);
	});

	// when filter button is pressed, close search panel and open filter panel
	$( '#filter-button' ).click( function() {
		$( '#filter-panel' ).slideToggle(200);
	});

	// when window scrolls, fix right hand/bottom header so it never scrolls above left hand/top header
	// when the screen is mobile sized
	$(window).scroll(function() {

		var currentScroll = $(window).scrollTop(); 

	    if (currentScroll >= calendar_grid_height) {
	        $('.right-bottom-header-box-interior').addClass('top-fixed');
	        $('#bud-nav').removeClass('bud-nav-normal');
	        $('#bud-nav').addClass('bud-nav-fixed');
	    } else {
	    	$('.right-bottom-header-box-interior').removeClass('top-fixed');
	    	$('#bud-nav').addClass('bud-nav-normal');
	    	$('#bud-nav').removeClass('bud-nav-fixed');
	    }
	});

	setCalendarHeight();

	/*Sliders*/
   // Smokes
    $("#id_smokes").slider();
    $("#id_smokes").on("slide", function(slideEvt) {
        var slide = slideEvt.value;
        var level = new Array("not", "a cheeky one", "social","regular","like a chimney");
        $("#smkSliderVal").text(level[slide]);
		$('#id_smokes').val(slide);
    });

    // Dancing
    $("#id_dances").slider();
    $("#id_dances").
    $("#id_dances").on("slide", function(slideEvt) {
        var slide = slideEvt.value;
        var level = new Array("toe tapping", "shoulder shuffle", "hip shaker", "arms waving", "get down");
        $("#ex1SliderVal").text(level[slide]);
		var t = $('#id_dances').val(slide);
        console.log('got here' + slide);
    });

    // Drinks
    $("#id_drinks").slider();
    $("#id_drinks").on("slide", function(slideEvt) {
		console.log('got here' + slideEvt.value);
        var slide = slideEvt.value;
        var level = new Array("teetotal", "social", "loads","too much","I have a problem");
        $("#dnkSliderVal").text(level[slide]);
		$('#id_drinks').val(slide);
    });

    // Involvment
    $("#id_involvement").slider();
    $("#id_involvement").on("slide", function(slideEvt) {
        var slide = slideEvt.value;
        var level = new Array("at the bar", "at the back", "next to stage","crowd surfing","mosh pit");
        $("#invSliderVal").text(level[slide]);
		var t = $('#id_involvement').val(slide);
        console.log('testing' + t);
    });

	var params = $( '#calendar-info' ).attr( 'data-month' ).split('-');
	var year = params[0];
	var month = params[1];
	
	loadCalendar(year, month, false);

});



var calendar_grid_height;

function setCalendarHeight() {
    var width = $( '#calendar-grid' ).width(); 
   	$( '.calendar-row' ).css('height', Math.floor(width * 0.14));
   	calendar_grid_height = $( '#left-top-box' ).height() - 75; 
}