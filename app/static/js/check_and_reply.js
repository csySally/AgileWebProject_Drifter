$(document).ready(function () {
  var params = new URLSearchParams(window.location.search);
  var label = params.get("label");
  var username = localStorage.getItem("username");
  if (label) {
    fetchNotesByLabel(label);
  } else {
    fetchRandomNote();
  }

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
  function fetchNotesByLabel(label) {
    $.ajax({
      url: "/api/random_note_by_label?label=" + encodeURIComponent(label),
      method: "GET",
      success: function (data) {
        if (data.body) {
          updateNoteContent(data);
        }
      },
      error: function (error) {
        console.error("Error fetching note by label:", error);
        alert("No notes found for this label.");
        window.location.href = "/user/" + username;
      },
    });
  }

  function updateNoteContent(data) {
    $("#noteContentContainer").html(data.body).data("send-id", data.id);
    $("#check-reply-user-img").attr("src", data.avatar_url);
    $("#check-reply-user p:last-child").text(
      data.anonymous ? "Anonymous" : data.author
    );
  }

  if (label) {
    fetchNotesByLabel(label);
  } else {
    fetchRandomNote();
  }

  $(document).on("click", "#check-next", function () {
    if (label) {
      fetchNotesByLabel(label);
    } else {
      fetchRandomNote();
    }
  });

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

  $(document).on("click", "#reply", function () {
    $("#reply-content").hide();
    $("#replyContainer").css("display", "block");
  });

  $(document).on("click", "#btn-send", function () {
    var replyBody = $("#replyInput").val();
    var isAnonymous = $("#flexCheckDefault").is(":checked");
    var username = localStorage.getItem("username");
    var sendId = $("#noteContentContainer").data("send-id");

    $.ajax({
      url: "/user/" + username + "/reply",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        reply_body: replyBody,
        anonymous: isAnonymous,
        note_id: sendId,
      }),
      success: function (response) {
        console.log("Reply sent successfully");
        alert("Reply sent successfully!");
        window.location.href = "/user/" + username;
      },
      error: function (error) {
        console.error("Error sending reply:", error);
      },
    });
  });
});
