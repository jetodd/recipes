$( document ).ready(function() {
	$('#select_all').click(function() {

		var checkBoxes = $("form input[type='checkbox']")
		console.log(checkBoxes)
		checkBoxes.attr( "checked" , true );
	});
});