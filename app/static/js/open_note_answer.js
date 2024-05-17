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

  var path = window.location.pathname;
  var segments = path.split("/");
  var noteId = segments[segments.length - 3];
  var replyId = segments[segments.length - 1];
  var username = segments[segments.length - 5];

  if (noteId && username && replyId) {
    fetchNoteAndReply(username, noteId, replyId);
  }

  function fetchNoteAndReply(username, noteId, replyId) {
    $.ajax({
      url: `/api/user/${username}/note/${noteId}/reply/${replyId}`,
      method: "GET",
      success: function (data) {
        console.log(data);
        displayNoteDetails(data);
      },
      error: function (error) {
        console.error("Failed to fetch note and reply details:", error);
      },
    });
  }

  function displayNoteDetails(data) {
    const note = data.note;
    const reply = data.reply;

    const noteContainer = document.getElementById("myNote");
    const replyContainer = document.getElementById("noteAnswer");
    const replyUsername = document.getElementById("reply-username");
    const replyUserAvatar = document.getElementById("reply-user-avatar");

    noteContainer.innerHTML = note.body;

    const userName = reply.anonymous ? "Anonymous" : reply.from_user;
    const userAvatarSrc = reply.anonymous
      ? "/static/images/default-avatar.png"
      : `/static/${reply.avatar_path}`;

    replyUsername.innerHTML = userName;
    replyContainer.innerHTML = reply.body;
    replyUserAvatar.src = userAvatarSrc;
  }
});
