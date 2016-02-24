/* DATE STUFF */

var currentDate;
var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
var dayNames = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
var numberEnds = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'];
var months = ['.row1 > .mon', '.row1 > .tue', '.row1 > .wed', '.row1 > .thu', '.row1 > .fri', '.row1 > .sat', '.row1 > .sun',
			'.row2 > .mon', '.row2 > .tue', '.row2 > .wed', '.row2 > .thu', '.row2 > .fri', '.row2 > .sat', '.row2 > .sun',
			'.row3 > .mon', '.row3 > .tue', '.row3 > .wed', '.row3 > .thu', '.row3 > .fri', '.row3 > .sat', '.row3 > .sun',
			'.row4 > .mon', '.row4 > .tue', '.row4 > .wed', '.row4 > .thu', '.row4 > .fri', '.row4 > .sat', '.row4 > .sun',
			'.row5 > .mon', '.row5 > .tue', '.row5 > .wed', '.row5 > .thu', '.row5 > .fri', '.row5 > .sat', '.row5 > .sun',
			'.row6 > .mon', '.row6 > .tue', '.row6 > .wed', '.row6 > .thu', '.row6 > .fri', '.row6 > .sat', '.row6 > .sun'];
/**
* Load a month into the calendar, provided with a name, the day on which it starts,
* in the format specified in dayNames, and the length of the month.
*/
var loadMonth = function(name, startDay, length, dayToSelect) {

	// show month name in bar above calendar
	$( '#month' ).html(name + ' ' + currentDate.getFullYear().toString());
	// get string for jquery look up of calendar cell corresponding to start day of month
	var index = months.indexOf('.row1 > .' + startDay);
	// remove existing gig classes and clear html
	$( '.gig' ).removeClass( 'gig' );
	$( '.gig > .calendar-circle > .calendar-text' ).html("");
	// remove existing today classes
	$( '.today' ).removeClass( 'today' );
	// add gig class to each cell in the month, and fill in the day number to the text part
	for (var i = index + dayToSelect - 1; i < length + index; i++) {
		$( months[i] + ' > .calendar-circle > .calendar-text').html(i - index + 1);
		$( months[i] ).toggleClass( 'gig' );
		if (i - index + 1 == dayToSelect) {
			$( months[i] ).addClass( 'today' );
			$( '#current-day' ).html($( '.today > .calendar-circle > .calendar-text' ).html());
		}
	}
}

function daysInMonth(month,year) {
    return new Date(year, month, 0).getDate();
}

/**
* Load the next month into the calendar.
*/
var loadNextMonth = function() {

	// get first of next month
	$( '.prev-month > img' ).toggle(true);
	var now = currentDate;
	if (now.getMonth() == 11) {
	    currentDate = new Date(now.getFullYear() + 1, 0, 1);
	} else {
	    currentDate = new Date(now.getFullYear(), now.getMonth() + 1, 1);
	}
	loadMonth(
		monthNames[currentDate.getMonth()], 
		dayNames[currentDate.getDay()], 
		daysInMonth(currentDate.getMonth() + 1, currentDate.getFullYear()), 
		1
	);
}

/**
* Load the previous month into the calendar.
*/
var loadPrevMonth = function() {

	// get first of next month
	var now = currentDate;
	var today = new Date();
	if (currentDate.getFullYear() == today.getFullYear() && currentDate.getMonth() == today.getMonth()) {
		return;
	}
	if (now.getMonth() == 0) {
	    currentDate = new Date(now.getFullYear() - 1, 11, 1);
	} else {
	    currentDate = new Date(now.getFullYear(), now.getMonth() - 1, 1);
	}
	if (currentDate.getFullYear() == today.getFullYear() && currentDate.getMonth() == today.getMonth()) {
		currentDate = new Date();
		loadMonth(
			monthNames[currentDate.getMonth()], 
			dayNames[new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay()], 
			daysInMonth(currentDate.getMonth() + 1, currentDate.getFullYear()), 
			currentDate.getDate()
		);
		$( '.prev-month > img' ).toggle(false);
	} else {
		loadMonth(
			monthNames[currentDate.getMonth()], 
			dayNames[currentDate.getDay()], 
			daysInMonth(currentDate.getMonth() + 1, currentDate.getFullYear()), 
			1
		);
	}
}



/* LAYOUT */

var load = function() {
	setCalendarHeight();
	   // get initial position of the element
	fixme2 = $( '#calendar-grid' ).height() + 15; 
	$( '#current-day' ).html($( '.today > .calendar-circle > .calendar-text' ).html());
	currentDate = new Date();
	loadMonth(
		monthNames[currentDate.getMonth()], 
		dayNames[new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay()], 
		daysInMonth(currentDate.getMonth() + 1, currentDate.getFullYear()), 
		currentDate.getDate()
	);
	$( '.prev-month > img' ).toggle(false);
	addClickListeners();
	/*$.getJSON( "http://api.songkick.com/api/3.0/metro_areas/24473-uk-glasgow/calendar.json?apikey=jwzmbEyCAIwD7HCy&per_page=45&page=1&perPage=1000&jsoncallback=?&per_page=50",
		function( data ) {
			var runningDay = data['resultsPage']['results']['event'][0]['start']['date'];
			$.each( data['resultsPage']['results']['event'], function(key, val) {
				$( '#filler' ).append(
					'<div class="gig-box"><div class="gig-info-box"><div class="act-name-box"><div class="act-name">' 
					+ val['performance'][0]['displayName'] 
					+ '</div></div><div class="venue-name-box"><div class="venue-name">' 
					+ val['venue']['displayName'] 
					+ '</div></div></div><div class="gig-time-box"><div class="gig-time">' 
					+ ((val['start']['time'] != null) ? val['start']['time'].substring(0, 5) : "")
					+ '</div></div></div>');
				if (val['start']['date'] != runningDay) {
					runningDay = val['start']['date'];
					$( '#filler' ).append('<div class="date-selector"><div class="scrolling-day-box ' + (val['start']['date']).split('').reverse().join('').substring(0, 2).split('').reverse().join('') + '">' + (val['start']['date']).split('').reverse().join('').substring(0, 2).split('').reverse().join('') + '</div></div>')
				}
			});
		});*/
}

$( document ).ready(load);

var addClickListeners = function() {
	for (var i = 0; i < months.length; i++) {
		$( months[i] ).click( function() {
			if ($( this ).hasClass( 'gig' ) == false) {
				return;
			}
			$( "." + $( '#current-day' ).html() ).parent().next().prevAll().toggle(true);
			$( '.today' ).removeClass( 'today' );
			$( this ).addClass( 'today' );
			$( '#current-day' ).html($( '.today > .calendar-circle > .calendar-text' ).html());
			$( "." + $( '#current-day' ).html() ).parent().next().prevAll().toggle(false);
		});
	}
	$( '.next-month' ).click( function() {
		loadNextMonth();
	})
	$( '.prev-month' ).click( function() {
		loadPrevMonth();
	})
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

	    if (currentScroll >= fixme2) {
	        $('.day-selector').addClass('top-fixed');
	    } else {
	    	$('.day-selector').removeClass('top-fixed');
	    }
	});
}

var fixme2;
var setCalendarHeight = function() {
    var width = $( '#calendar-grid' ).width(); 
   	$( '.calendar-row' ).css('height', Math.floor(width * 0.14));
   	fixme2 = $( '#calendar-grid' ).height() + 15; 
}

window.onresize = function(event) {
    setCalendarHeight();
};