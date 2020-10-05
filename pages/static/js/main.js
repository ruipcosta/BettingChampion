function viewtips() {
  // disable button
  $("#btn-viewtips").prop("disabled", true);
  // add spinner to button
  $("#btn-viewtips").html(
    `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Loading...`
  );
  window.location.href = "games/";
}

function refreshDatabase() {
  $.ajax({
    url: "updating/",
    success: function (response) {
      $("p").remove();
      $(response).appendTo("body");
    },
  });
}

function allGames() {
  $(".title").fitText(0.8);
  // $(".info").fitText(0.6);
  updateDatabase();
}

function updateDatabase() {
  $.ajax({
    url: "updating/",
    success: function (response) {
      console.log(response[0]);
    },
  });
}
