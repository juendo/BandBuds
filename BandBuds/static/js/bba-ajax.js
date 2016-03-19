$( document ).ready( function() {

	// I'm Going button pressed 
	$( '#im-going' ).click( function(){
	    var gig_id = $( this ).data( 'gigid' );
	    $.get('../../ajax/im_going/' + gig_id, function(response) {
	        $( '#im-going' ).html(response);
	        $( '#im-going' ).toggleClass( 'not-going-button' );
	    });
	});

	// when a cell in the calendar is clicked, load gigs for that day into
	// the list of gigs, and update UI
	$( '.calendar-cell' ).click( function() {

		// if the cell is empty do nothing
		if (!$( this ).hasClass( 'gig' )) {
			return;
		}
		// make the pressed cell today
		$( '.today' ).removeClass( 'today' );
		$( this ).addClass( 'today' );
		$( '#current-day' ).html( $( this ).attr( 'data-day' ) );
		loadGigs();
	});

	/*
	* When the right arrow is pressed to load the next month into the calendar.
	*/
	$( '.next-month' ).click( function() {

		// extract the current month and year
		var params = $( '#calendar-info' ).attr( 'data-month' ).split('-');
		var year = params[0];
		var month = params[1];

		// get the next month and year
		month = ((parseInt(month) % 12) + 1);
		if (month == 1) {
			year++;
		}
		loadCalendar(year, month);
	});

	/*
	* When the right arrow is pressed to load the next month into the calendar.
	*/
	$( '.prev-month' ).click( function() {

		if (!$( '.prev-month > img' ).is( ':visible' )) {
			return;
		}

		// extract the current month and year
		var params = $( '#calendar-info' ).attr( 'data-month' ).split('-');
		var year = params[0];
		var month = params[1];

		// get the next month and year
		month = ((parseInt(month) + 10) % 12 + 1);
		if (month == 12) {
			year--;
		}
		loadCalendar(year, month);
	});

	$( '#bud-filter' ).click( function() {
		var params = $( '#calendar-info' ).attr( 'data-month' ).split('-');
		var year = params[0];
		var month = params[1];
		loadCalendar(year, month);
	});

	$( '.nudge' ).click( function() {
		var username = $( this ).data( 'user' );
		var gigid = $( this ).data( 'gigid' );
		var button = $( this );
		$.get(
			'/ajax/nudge/' + username + '/' + gigid,
			{},
			function(data) {
				button.html(data);
			}
		)
	});

	$('.search').click()

    // Tool tip, Hover over button with dataitoggle att. to show what link/button dose
    $('[data-toggle="tooltip"]').tooltip();

    /*Sliders*/
    $("#ex1").slider();
    $("#ex1").on("slide", function(slideEvt) {
        $("#ex1SliderVal").text(slideEvt.value);
    });
    // With JQuery
    $("#ex14").slider({
        ticks: [0, 100, 200, 300, 400],
        ticks_positions: [0, 30, 60, 70, 90, 100],
        ticks_labels: ['$0', '$100', '$200', '$300', '$400'],
        ticks_snap_bounds: 30
    });

   // With JQuery
    $("#ex4").slider({
        reversed : true
    });
});





// HELPERS

// load the gigs for the current day
function loadGigs() {

	var with_buds = $( '#bud-filter' ).is( ':checked' ) ? 't' : 'f';

	// send the ajax request
	$.get(
		'/ajax/load_gigs/' + $( '#calendar-info' ).attr( 'data-month' ) + '-' + $( '.today' ).attr( 'data-day' ) + '/' + with_buds, 
		{}, 
		// load the response html into the list of gigs
		function(data) {
	        $( '#list-box' ).html(data);
	   	}
	);
}

// reload the calendar for a given year and month
function loadCalendar(year, month) {

	var with_buds = $( '#bud-filter' ).is( ':checked' ) ? 't' : 'f';

	// send ajax request to get json for reloading calendar
	$.get(
		'../../ajax/reload_calendar/' + year + '-' + month + '-1/' + with_buds, 
		{}, 
		function(data) {
			// load new calendar details
	        loadCalendarFromJson(data.calendar);

	        // update UI to reflect new date
	        $( '#month' ).html( data.month_string );
	        $( '#current-day' ).html( data.day_string );

	        // store new date as data field in calendar info div
	        $( '#calendar-info' ).attr( 'data-month', data.month_string );

	        // hide previous button if necessary
	        $( '.prev-month > img' ).toggle(!data.prev_hidden);

	        // load gigs for new date
	        loadGigs();
	   	}
	);
}

// load a 2D array of day numbers into the calendar
function loadCalendarFromJson(calendar) {

	// clear the current day
	$( '.today' ).removeClass( '.today' );

	// boolean to track whether the first day has been found yet
	var found = false;

	// get the rows of the calendar
	var rows = $( ".calendar-row" ).toArray();

	// for each row
	for (var i = 0; i < 6; i++) {

		// (skipping the first as it contains the day names)
		var cells = rows[i + 1].children;

		// and for each cell in that row
		for (var j = 0; j < 7; j++) {

			// update the day data
			cells[j].setAttribute('data-day', calendar[i][j]);

			// add classes appropriately
			if (calendar[i][j] == 0) {
				cells[j].className = 'calendar-cell';
				cells[j].children[0].children[0].innerHTML = "";
			} else if (found == false) {
				cells[j].className = 'calendar-cell gig today';
				cells[j].children[0].children[0].innerHTML = calendar[i][j];
				found = true;
			} else {
				cells[j].className = 'calendar-cell gig';
				cells[j].children[0].children[0].innerHTML = calendar[i][j];
			}
		}
	}
}