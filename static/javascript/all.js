/* AutoComplete */
$(function(){
	var course_list = []
	$.getJSON("/courses", function(data){
		$.each(data, function(i,item) {
			course_list.push(item);
		});

		$('#courses').autocomplete({
			source: course_list
		});
	});
	
});




/* Buttons */


/*New Button */
$(function(){
	//check the fall button
	$('input:radio[name=toggle]')[0].checked = true;
	$("#fall").addClass('select');

	$(".b-style").click(function(){
		$(".b-style").removeClass('select');
		$(this).addClass('select');
	});
});

/* Hide the div initially */
$(document).ready(function() {
	$('#sched').hide();
});






/* Ajax Submit 
$(document).ready(function() {
	var options = {
		target: '#output_schedule',
		beforeSubmit: showRequest

	};

	$('#searchcourses').submit(function () {
		$(this).ajaxSubmit(options);

		return false;
	});
});

function showRequest(formData, jqForm, options) {
	var queryString = $.param(formData);
	//check to see if the course is selected
	if (!formData[0].value) {
		alert('Please select a course');
		return false;
	}

	alert('About to submit: \n\n' + queryString);

	return false;
}

*/






