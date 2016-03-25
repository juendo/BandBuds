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
		loadCalendar(year, month, false);
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
		// final field is true as we want to load the final day of the previous month
		// in case user is using back button on day nav
		loadCalendar(year, month, true);
	});

	$( '#bud-filter' ).click( function() {
		var params = $( '#calendar-info' ).attr( 'data-month' ).split('-');
		var year = params[0];
		var month = params[1];
		loadCalendar(year, month, false);
	});

	$( '#search-text' ).keyup( function() {
		var params = $( '#calendar-info' ).attr( 'data-month' ).split('-');
		var year = params[0];
		var month = params[1];
		var search = $( '#search-text' ).val();
		loadCalendar(year, month, false);
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

    // Likes
	$( document ).on( 'click', '.band', function() {

	    var bandid = $( this ).attr( "data-bandid" );
		var bandslug = $( this ).attr( "data-bandslug" )
	    var userid = $( this ).attr( "data-user" );
		var opinion = $( this ).attr( "data-like" );

		$.get(
			'/ajax/' + opinion + '_band/', 
			{ user_id: userid, band_id: bandid }, 
			function (data) {
				$('.' + bandslug).html(data);
				$('.' + bandslug).addClass($('.' + bandslug + ' > #like').attr( 'data-bandslug' ));
				$('.' + bandslug).removeClass( '.' + bandslug )
			}
		);
	});

	//nudge
	$('.nudge').click(function() {

		var userid = $(this).attr("data-userid");
		var budid = $(this).attr("data-budid");
    	var gigid = $(this).attr("data-gigid");
		var button = $( this );

		$.get(
			'/ajax/nudge/',
			{user_id:userid,bud_id: budid, gig_id : gigid},
			function(data) {
				button.html(data);
				button.toggleClass( 'nudged' );
			}
		)


	});

	// when the next day arrow is clicked in the calendar day nav
	$( '.next-day' ).click( function() {
		// get the day number of the next day with gigs from today
		var next = $( '.today' ).attr( 'data-next' );
		// if there is such a day
		if (next != null && next.length > 0) {
			// act as if the cell corresponding to that day was clicked
			$( '.cell-' + next ).click();
		} else {
			// otherwise load the next month
			$( '.next-month' ).click();
		}
	});

	// when the previous day arrow is clicked in the calendar day nav
	$( '.prev-day' ).click( function() {
		// get the day number of the previous day with gigs from today
		var prev = $( '.today' ).attr( 'data-prev' );
		// if there is such a day
		if (prev != null && prev.length > 0) {
			// act as if the cell corresponding to that day was clicked
			$( '.cell-' + prev ).click();
		} else {
			// otherwise load the previous month
			$( '.prev-month' ).click();
		}
	});

	$( '.accept' ).click( function() {
		var gigid = $( this ).attr( 'data-gigid' );
		var bud = $( this ).attr( 'data-bud' );
		$.ajax({
			type: 'GET',
			url: '/ajax/accept/',
			data: { 'gigid' : gigid, 'bud' : bud },
			success: function(data) {
				$( '.' + bud + '.gig-' + gigid ).remove();
			}
		});
	});

	$( '.decline' ).click( function() {
		var gigid = $( this ).attr( 'data-gigid' );
		var bud = $( this ).attr( 'data-bud' );
		$.ajax({
			type: 'GET',
			url: '/ajax/decline/',
			data: { 'gigid' : gigid, 'bud' : bud },
			success: function(data) {
				$( '.' + bud + '.gig-' + gigid ).remove();
			}
		});
	});

});





// HELPERS

// load the gigs for the current day
function loadGigs() {

	console.log()

	var with_buds = $( '#bud-filter' ).is( ':checked' ) ? 't' : 'f';

	var search = $( '#search-text' ).val();

	var month = $( '#calendar-info' ).attr( 'data-month' );

	var day = $( '.today' ).attr( 'data-day' );

	if (!day) {
		day = '1';
	}

	// send the ajax request
	$.ajax({
		type: 'GET',
		url: '/ajax/load_gigs/' + month+ '-' + day + '/' + with_buds,
		data: { 'search' :  search },
		// load the response html into the list of gigs
		success: function(data) {
			$( '#list-box' ).html(data);
		}
	});
}

// reload the calendar for a given year and month
function loadCalendar(year, month, selectLast) {

	var with_buds = $( '#bud-filter' ).is( ':checked' ) ? 't' : 'f';

	var search = $( '#search-text' ).val();

	// send ajax request to get json for reloading calendar
	$.ajax({
		type: 'GET',
		url: '../../ajax/reload_calendar/' + year + '-' + month + '-1/' + with_buds,
		data: { 'search' : search },
		success: function(data) {
			

	        // update UI to reflect new date
	        $( '#month' ).html( data.month_string );
	        $( '#current-day' ).html( data.day_string );

	        // store new date as data field in calendar info div
	        $( '#calendar-info' ).attr( 'data-month', data.month_string );

	        // hide previous button if necessary
	        $( '.prev-month > img' ).toggle(!data.prev_hidden);

	        // load new calendar details
	        loadCalendarFromJson(data.calendar, selectLast);

	        // load gigs for new date
	        loadGigs();
	        
		}
	})
}

// load a 2D array of day numbers into the calendar, expected in the form
// [[0,0,0,1,2,3,4], [5,6,7,0,0,10,11]]... etc, with 0s for days with no gigs
// select last is a boolean parameter for whether to make today the last day of the month
// instead of the first
function loadCalendarFromJson(calendar, selectLast) {

	// clear the current day
	$( '.today' ).removeClass( '.today' );

	// boolean to track whether the first day has been found yet
	var found = false;

	// get the rows of the calendar
	var rows = $( ".calendar-row" ).toArray();

	// used to track the previous day which has gigs
	var prevDay = null;

	// for each row
	for (var i = 0; i < 6; i++) {

		// (skipping the first as it contains the day names)
		var cells = rows[i + 1].children;

		// and for each cell in that row
		for (var j = 0; j < 7; j++) {

			// update the day data
			cells[j].setAttribute('data-day', calendar[i][j]);
			// add classes and data appropriately:

			// if the day has no gigs
			if (calendar[i][j] == 0) {
				// set the text to 0
				cells[j].className = 'calendar-cell';
				cells[j].children[0].children[0].innerHTML = "";
			} 
			// otherwise, if this is the first day with gigs
			else if (found == false) {
				// clear the previous and next day data
				cells[j].setAttribute('data-prev', '');
				cells[j].setAttribute('data-next', '');
				// add classes, including 'today' representing the current day, and display the day number
				cells[j].className = 'calendar-cell gig today cell-' + calendar[i][j];
				cells[j].children[0].children[0].innerHTML = calendar[i][j];
				// store reference to day
				prevDay = cells[j];
				found = true;
			} 
			// otherwise, if it is a subsequent day with gigs
			else {
				// clear the previous and next day data
				cells[j].setAttribute('data-prev', '');
				cells[j].setAttribute('data-next', '');
				// set the next day attribute of the previous day
				prevDay.setAttribute('data-next', cells[j].getAttribute('data-day'));
				// and the previous day attribute of this day
				cells[j].setAttribute('data-prev', prevDay.getAttribute('data-day'));
				cells[j].className = 'calendar-cell gig cell-' + calendar[i][j];
				cells[j].children[0].children[0].innerHTML = calendar[i][j];
				prevDay = cells[j];
			}
		}
	}

	if (selectLast) {
		prevDay.click();
	}
}