
$(document).ready(function () {
	/* AutoComplete */
	$('input.course').typeahead({
	    name: 'courses',
	    prefetch: '../courses.json',
	    limit: 10
	});



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

	/* Colorbox */
	$('.about').colorbox({ rel: 'about', width: '600px'});
});







