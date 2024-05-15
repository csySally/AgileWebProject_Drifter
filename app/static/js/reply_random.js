// after users open the envelop, can check the note
$(document).ready(function () {
  $.ajax({
    url: "/get_user_info",
    type: "GET",
    success: function (response) {
      $("#username").text(response.username);
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });

  function fetchRandomNote() {
    $.ajax({
      url: "/api/random_other_note",
      method: "GET",
      success: function (data) {
        console.log(data);
        // updateNoteContent(data);
      },
      error: function (error) {
        console.error("Error fetching next note:", error);
      },
    });
  }
  $(document).on("click", "#open", function () {
    fetchRandomNote();
  });

  /*   function updateNoteContent() {
    $("#noteContentContainer").html(data.body);
    $("#check-reply-user img").attr(
      "src",
      data.anonymous
        ? "../static/images/default-avatar.png"
        : "../static/images/user-avatar/" + data.author + ".png"
    );
    $("#check-reply-user p:last-child").text(
      data.anonymous ? "From: Anonymous" : "From: " + data.author
    );
  }
 */

  // click close note button to return to the reply_note_entry page
  $(document).on("click", "#close-note", function () {
    window.location.href = "../templates/reply_note_entry.html";
  });

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
