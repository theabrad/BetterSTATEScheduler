jQuery(document).ready(function($) {
  $('a[rel*=facebox]').facebox() 
});

/* AutoComplete */
$(function(){
	var course_list = []
	$.getJSON("/courses", function(data){
		$.each(data, function(i,item) {
			course_list.push(item);
		});
		
		$('#courses').autocompleteArray(course_list, {
			autoFill: false,
			cacheLength: 10,
			matchContains: 1
		});
		
	});
	
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







