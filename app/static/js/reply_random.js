// after users open the envelop, can check the note
$(document).ready(function () {
  $("#open").on("click", function (event) {
    $.ajax({
      url: "../templates/check_and_reply.html",
      success: function (html) {
        $("#contentContainer").html(html);
      },
      error: function (error) {
        console.error("Error loading check_and_reply.html:", error);
      },
    });
  });

  // click close note button to return to the reply_note_entry page
  $(document).on("click", "#close-note", function () {
    window.location.href = "../templates/reply_note_entry.html";
  });
});
