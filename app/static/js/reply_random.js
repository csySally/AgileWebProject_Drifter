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
