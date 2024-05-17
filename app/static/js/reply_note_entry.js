$(document).ready(function () {
  $.ajax({
    url: "/get_user_info",
    type: "GET",
    success: function (response) {
      $("#username").text(response.username);
      localStorage.setItem("username", response.username);
      var storedUsername = localStorage.getItem("username");

      backToIndex(storedUsername);
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });

  /* return to the index when click the btn-close button */
  function backToIndex(username) {
    document.querySelector(".btn-close").addEventListener("click", function () {
      window.location.href = "/user/" + username;
    });
    document.querySelector(".logo-link").addEventListener("click", function () {
      window.location.href = "/user/" + username;
    });
  }
  $("#search").on("click", () => {
    $("#cover").css("display", "block");
    $("#search-label-card").css("display", "block");
  });

  $("#search-input").on("keyup", () => {
    const searchInput = $("#search-input").val();
    if (searchInput.length > 0) {
      $("#search-label-btn").prop("disabled", false);
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

  /* search for a label */
  $(document).on("click", "#search-label-btn", function () {
    var label = $("#search-input").val().trim();
    if (label) {
      window.location.href =
        "/reply-note-check?label=" + encodeURIComponent(label);
    } else {
      alert("Please enter a label to search.");
    }
  });
});
