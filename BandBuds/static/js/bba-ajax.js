var calendar_grid_height;

function setCalendarHeight() {
    var width = $( '#calendar-grid' ).width(); 
   	$( '.calendar-row' ).css('height', Math.floor(width * 0.14));
   	calendar_grid_height = $( '#left-top-box' ).height() - 75; 
}

$( document ).ready( function() {

	$( window ).resize(function(event) {
	    setCalendarHeight();
	});

	$('#going-button').click(function(){
	    var goingid;
	    goingid = $(this).attr("data-goingid");
	    $.get('/bba/gig_attending/', {gig_id: goingid}, function(data){
	               $('#going').html(data);
	               $('#going-button').hide();
	    });
	});

	$( '.calendar-cell' ).click(function() {

		if (!$( this ).hasClass( 'gig' )) {
			return;
		}
		$( '.today' ).removeClass( 'today' );
		$( this ).addClass( 'today' );
		$( '#current-day' ).html($( '.today > .calendar-circle > .calendar-text' ).html());
		$.get(
			'/load_gigs/' + $( '#month' ).html() + '-' + $( '#current-day' ).html(), 
			{}, 
			function(data) {
	            $('#list-box').html(data);
	    	}
	    );
	});

	$( '.next-day' ).click( function() {
		setCurrentDay(parseInt($( '#current-day' ).html()) + 1);
	});
	$( '.prev-day' ).click( function() {
		setCurrentDay(parseInt($( '#current-day' ).html()) - 1);
	});
	
	$( '#search-button' ).click( function() {
		if ($( '#filter-panel' ).is(':visible')) {
			$( '#filter-panel').slideToggle(200, function() {
				$( '#search-panel' ).slideToggle(200);
			});
		} else {
			$( '#search-panel' ).slideToggle(200);
		}
	});
	$( '#filter-button' ).click( function() {
		if ($( '#search-panel' ).is(':visible')) {
			$( '#search-panel').slideToggle(200, function() {
				$( '#filter-panel' ).slideToggle(200);
			});
		} else {
			$( '#filter-panel' ).slideToggle(200);
		}
	});
	$(window).scroll(function() {

		var currentScroll = $(window).scrollTop(); 

	    if (currentScroll >= calendar_grid_height) {
	        $('.day-selector').addClass('top-fixed');
	    } else {
	    	$('.day-selector').removeClass('top-fixed');
	    }
	});

	$( '.next-month' ).click( function() {
		loadNextMonth();
	})
	$( '.prev-month' ).click( function() {
		loadPrevMonth();
	})

});

	