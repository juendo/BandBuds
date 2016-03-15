$( document ).ready( function() {

		// scale calendar so cells retain circular proportion when window is resized.
	$( window ).resize(function(event) {
	    setCalendarHeight();
	});

	// when search button pressed, close filter panel and open search panel
	$( '#search-button' ).click( function() {
		if ($( '#filter-panel' ).is(':visible')) {
			$( '#filter-panel').slideToggle(200, function() {
				$( '#search-panel' ).slideToggle(200);
			});
		} else {
			$( '#search-panel' ).slideToggle(200);
		}
	});

	// when filter button is pressed, close search panel and open filter panel
	$( '#filter-button' ).click( function() {
		if ($( '#search-panel' ).is(':visible')) {
			$( '#search-panel').slideToggle(200, function() {
				$( '#filter-panel' ).slideToggle(200);
			});
		} else {
			$( '#filter-panel' ).slideToggle(200);
		}
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
});



var calendar_grid_height;

function setCalendarHeight() {
    var width = $( '#calendar-grid' ).width(); 
   	$( '.calendar-row' ).css('height', Math.floor(width * 0.14));
   	calendar_grid_height = $( '#left-top-box' ).height() - 75; 
}