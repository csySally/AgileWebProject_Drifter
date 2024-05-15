$(document).ready(function () {
  function fetchRandomNote() {
    $.ajax({
      url: "/api/random_other_note",
      method: "GET",
      success: function (data) {
        console.log(data);
        updateNoteContent(data);
      },
      error: function (error) {
        console.error("Error fetching next note:", error);
      },
    });
  }

  function updateNoteContent(data) {
    $("#noteContentContainer").html(data.body);
    $("#check-reply-user-img").attr("src", data.avatar_url);
    $("#check-reply-user p:last-child").text(
      data.anonymous ? "Anonymous" : data.author
    );
  }

  fetchRandomNote();

  $(document).on("click", "#check-next", function () {
    fetchRandomNote();
  });

  // click close note button to return to the reply_note_entry page
  $.ajax({
    url: "/get_user_info",
    type: "GET",
    success: function (response) {
      $("#username").text(response.username);
      localStorage.setItem("username", response.username);

      var storedUsername = localStorage.getItem("username");
      console.log("Stored Username:", storedUsername);

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

  $(document).on("click", ".btn-close", function () {
    $("#contentContainer").empty();
  });

  $(document).on("click", "#check-next", function () {
    fetchRandomNote();
  });

  $(document).on("click", "#reply", function () {
    $("#reply-content").hide();
    $("#replyContainer").css("display", "block");
  });
});
