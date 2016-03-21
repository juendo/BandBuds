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
	$('.band').click(function(){

	    var bandid = $(this).attr("data-bandid");
		var bandslug = $(this).attr("data-bandslug")
	    var userid= $(this).attr("data-user");
		var opinion=$(this).attr("id");
		console.log('band button'+ bandslug+' and '+ userid + ' '+ opinion);
		$.get('/profile/'+opinion+'_band/', {user_id: userid, band_id: bandid}, function (data) {
			$('.' + bandslug).hide();
		});
	});

	//nudge
	$('.nudge').click(function() {

		var userid= $(this).attr("data-userid");
		var budid = $(this).attr("data-budid");
    	var gigid= $(this).attr("data-gigid");
		var button = $( this );

		//url(r'^ajax/nudge/(?P<user_slug>[\w\-]+)/(?P<gig_id>[0-9]+)$', views.nudge, name='nudge'),

		console.log(userid+ ' ' + budid + ' '+ gigid + ' ' + '/ajax/nudge/' + budid + '/' + gigid+ '/');
		$.get(
			'/ajax/nudge/',
			{user_id:userid,bud_id: budid, gig_id : gigid},
			function(data) {
				button.html(data);
			}
		)


	});

	$( '.next-day' ).click( function() {
		var next = $( '.today' ).attr( 'data-next' );
		if (next != null && next.length > 0) {
			$( '.cell-' + next ).click();
		} else {
			$( '.next-month' ).click();
		}
	});

	$( '.prev-day' ).click( function() {
		var prev = $( '.today' ).attr( 'data-prev' );
		if (prev != null && prev.length > 0) {
			$( '.cell-' + prev ).click();
		} else {
			$( '.prev-month' ).click();
		}
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

// load a 2D array of day numbers into the calendar
function loadCalendarFromJson(calendar, selectLast) {

	// clear the current day
	$( '.today' ).removeClass( '.today' );

	// boolean to track whether the first day has been found yet
	var found = false;

	// get the rows of the calendar
	var rows = $( ".calendar-row" ).toArray();

	// used to track the previous and next days for the cells
	var prevDay = null;
	var nextDay = null;

	// for each row
	for (var i = 0; i < 6; i++) {

		// (skipping the first as it contains the day names)
		var cells = rows[i + 1].children;

		// and for each cell in that row
		for (var j = 0; j < 7; j++) {

			// update the day data
			cells[j].setAttribute('data-day', calendar[i][j]);
			// add classes and data appropriately
			if (calendar[i][j] == 0) {
				cells[j].className = 'calendar-cell cell-' + calendar[i][j];
				cells[j].children[0].children[0].innerHTML = "";
			} else if (found == false) {
				cells[j].setAttribute('data-prev', '');
				cells[j].setAttribute('data-next', '');
				cells[j].className = 'calendar-cell gig today cell-' + calendar[i][j];
				cells[j].children[0].children[0].innerHTML = calendar[i][j];
				prevDay = cells[j];
				found = true;
			} else {
				cells[j].setAttribute('data-prev', '');
				cells[j].setAttribute('data-next', '');
				prevDay.setAttribute('data-next', cells[j].getAttribute('data-day'));
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