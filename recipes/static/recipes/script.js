$(document).ready(function() {
	$('#select_all').click(function() {
		var checkBoxes = $("form input[type='checkbox']")
		checkBoxes.attr( "checked" , true );
	});

	$('#toggle_search').click(function() {
		const searchForm = $('#search_form')
		$('#search_form').toggleClass('show');
		$('.search_input').focus();
	});
});