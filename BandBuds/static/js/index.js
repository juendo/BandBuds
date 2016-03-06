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
		$( months[i] ).addClass( 'day-' + (i - index + 1));

		if (i - index + 1 == dayToSelect) 
		{
			$( months[i] ).addClass( 'today' );
			$( '#current-day' ).html($( '.today > .calendar-circle > .calendar-text' ).html());
		}
	}
}

function daysInMonth(month,year) 
{
    return new Date(year, month, 0).getDate();
}

// Set the current day for which to view gigs.
// Act in the same way as if that day were clicked on the calendar.
function setCurrentDay(day) 
{
	$( '.day-' + day ).trigger( 'click' );
}

/* LAYOUT */

var load = function() {

	setCalendarHeight();
	// get initial position of the element
	//calendar_grid_height = $( '#calendar-grid' ).height() + 15; 

	currentDate = new Date($( '#month' ).html() + '-' + $('#current-day').html());

	loadMonth(
		monthNames[currentDate.getMonth()], 
		dayNames[new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay()], 
		daysInMonth(currentDate.getMonth() + 1, currentDate.getFullYear()), 
		currentDate.getDate()
	);

	var now = new Date();

	if (currentDate.getMonth() == now.getMonth() && currentDate.getFullYear() == now.getFullYear()) {
		$( '.prev-month > img' ).toggle(false);
	}
}

$( document ).ready(load);

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

