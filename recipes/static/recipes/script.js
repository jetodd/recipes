$(document).ready(function () {
  $('#select_all').click(function () {
    const checkBoxes = $("form input[type='checkbox']")

    if (checkBoxes.filter(':checked').length === checkBoxes.length) {
      checkBoxes.attr("checked", false);
    } else {
      checkBoxes.attr("checked", true);
    }
  });

  $('#toggle_search').click(function () {
    $('#search_form').toggleClass('show');
    $('.search_input').focus();
  });

  const thisWeek = document.getElementById('this-week');

  const options = {
    animation: 150,
    ghostClass: 'drag-and-drop-ghost',
    handle: '.fa-paw'
  }

  function saveFormAsync(form) {
    fetch(form.action, {
      body: new FormData(form),
      method: 'POST'
    })
      .catch(console.error)
  }

  function updatePositionHiddenInput(list, formInput) {
    const rows = list.querySelectorAll('li');
    let ids = [];
    for (let row of rows) {
      ids.push(row.dataset.recipeId);
    }
    formInput.value = ids.join(',');
  }

  if (thisWeek) {
    const form = document.getElementById('this-week-frm');
    const formInput = document.getElementById('thisWeekPositionInput');

    function saveThisWeek() {
      updatePositionHiddenInput(thisWeek, formInput);
      saveFormAsync(form);
    }

    Sortable.create(thisWeek, {...options, onEnd: saveThisWeek});
  }

  const nextWeek = document.getElementById('next-week');
  if (nextWeek) {
    const form = document.getElementById('next-week-frm');
    const formInput = document.getElementById('nextWeekPositionInput');

    function saveNextWeek() {
      updatePositionHiddenInput(nextWeek, formInput);
      saveFormAsync(form);
    }

    Sortable.create(nextWeek, {...options, onEnd: saveNextWeek});
  }
});

