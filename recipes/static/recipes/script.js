$(document).ready(function () {
  $('#select_all').click(function () {
    const checkBoxes = $("form input[type='checkbox']")
    checkBoxes.attr("checked", true);
  });

  $('#toggle_search').click(function () {
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

    const saveOrderingButton = document.getElementById('saveThisWeekBtn');
    const form = document.getElementById('this-week-frm');
    const formInput = document.getElementById('thisWeekPositionInput');

    function saveOrdering() {
      const rows = thisWeek.querySelectorAll('li');
      let ids = [];
      for (let row of rows) {
        ids.push(row.dataset.recipeId);
      }
      formInput.value = ids.join(',');
      form.submit();
    }

    saveOrderingButton.addEventListener('click', saveOrdering);
  }

  const nextWeek = document.getElementById('next-week');
  if (nextWeek) {
    Sortable.create(nextWeek, options);

    const saveOrderingButton = document.getElementById('saveNextWeekBtn');
    const form = document.getElementById('next-week-frm');
    const formInput = document.getElementById('nextWeekPositionInput');

    function saveOrdering() {
      const rows = nextWeek.querySelectorAll('li');
      let ids = [];
      for (let row of rows) {
        ids.push(row.dataset.recipeId);
      }
      formInput.value = ids.join(',');
      form.submit();
    }

    saveOrderingButton.addEventListener('click', saveOrdering);
  }
});

