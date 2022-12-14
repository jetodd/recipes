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

	const thisWeek = document.getElementById('this-week');

	const options = {
		animation: 150,
		ghostClass: 'drag-and-drop-ghost'
	}

	if (thisWeek) {
		Sortable.create(thisWeek, options);
	}

	const nextWeek = document.getElementById('next-week');
	if (nextWeek) {
		Sortable.create(nextWeek, options);
	}
});

