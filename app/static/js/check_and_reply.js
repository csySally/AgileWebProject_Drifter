$(document).ready(function () {
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

  function fetchRandomNote() {
    $.ajax({
      url: "#",
      method: "GET",
      success: function (data) {
        updateNoteContent(data);
      },
      error: function (error) {
        console.error("Error fetching next note:", error);
      },
    });
  }

  $(document).on("click", "#reply", function () {
    $("#reply-content").hide();
    $("#replyContainer").css("display", "block");
  });
});
