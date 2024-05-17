$(document).ready(function () {
  $.ajax({
    url: "/get_user_info",
    type: "GET",
    success: function (response) {
      $("#username").text(response.username);
      localStorage.setItem("username", response.username);
      var storedUsername = localStorage.getItem("username");

      backToIndex(storedUsername);
      fetchNotesAndReplies(storedUsername);
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

  /* fetch notes and their replies */
  function fetchNotesAndReplies(username) {
    $.ajax({
      url: "/user/" + username + "/sent_notes",
      method: "GET",
      success: function (response) {
        displayEnvelopes(response.notes_with_replies);
      },
      error: function (error) {
        console.error("Failed to fetch notes and replies:", error);
      },
    });
  }

  /* display all the replies in the envelops */
  function displayEnvelopes(notesWithReplies) {
    const container = $("#reply-envelop");
    container.empty(); // Clear existing content

    notesWithReplies.forEach((note) => {
      note.replies.forEach((reply) => {
        container.append(
          '<a href="/templates/open_note_answer.html"><img src="../static/images/reply_envelop.png" alt="Reply Envelope" /></a>'
        );
      });
    });
  }

  // Initial fetch of notes and replies
  fetchNotesAndReplies();
});
