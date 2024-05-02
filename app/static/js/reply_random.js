// after users open the envelop, can check the note
$(document).ready(function () {
  $("#open").on("click", function (event) {
    $.ajax({
      url: "../templates/check_and_reply.html",
      success: function (html) {
        $("#contentContainer").html(html);
      },
      error: function (error) {
        console.error("Error loading note.html:", error);
      },
    });
  });
});
