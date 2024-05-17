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
      console.log("Error fetching user info:", error);
    },
  });

  function backToIndex(username) {
    document.querySelector(".btn-close").addEventListener("click", function () {
      window.location.href = "/user/" + username;
    });
    document.querySelector(".logo-link").addEventListener("click", function () {
      window.location.href = "/user/" + username;
    });
  }

  function fetchNotesAndReplies(username) {
    if (!username) {
      console.error("Username not available for fetching notes and replies.");
      return;
    }
    console.log("Fetching notes for username:", username);
    $.ajax({
      url: `/api/user/${username}/notes_with_replies`,
      method: "GET",
      success: function (response) {
        displayEnvelopes(response.notes_with_replies, username);
      },
      error: function (xhr, status, error) {
        console.error("Failed to fetch notes and replies:", xhr.responseText);
      },
    });
  }

  function displayEnvelopes(notesWithReplies, username) {
    console.log("Notes with replies:", notesWithReplies);
    const container = $("#reply-envelop");
    container.empty();

    notesWithReplies.forEach((item) => {
      if (item.replies.length > 0) {
        item.replies.forEach((reply) => {
          const replyDetailUrl = `/user/${username}/note/${item.note.id}/reply/${reply.id}`;
          container.append(
            `<a href="${replyDetailUrl}"><img src="../static/images/reply_envelop.png" alt="View Reply"></a>`
          );
        });
      }
    });
  }
});
