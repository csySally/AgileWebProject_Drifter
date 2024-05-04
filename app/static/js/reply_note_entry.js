$(document).ready(function () {
  $(".btn-close").on("click", () => {
    window.location.href = "../templates/index.html";
  });

  $("#search").on("click", () => {
    $("#cover").css("display", "block");
    $("#search-label-card").css("display", "block");
  });

  $("#search-input").on("keyup", () => {
    const searchInput = $("#search-input").val();
    if (searchInput.length > 0) {
      $("#search-label-btn").prop("disabled", false);
      $("#search-label-btn").on("click", () => {
        window.location.href = "../templates/check_and_reply.html";
      });
      // after return key is pressed, can also trigger the click event
      $("#search-input").on("keypress", (e) => {
        if (e.which === 13) {
          $("#search-label-btn").trigger("click");
        }
      });
    } else {
      $("#search-label-btn").prop("disabled", true);
    }
  });
});
