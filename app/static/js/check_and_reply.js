$(document).ready(function () {
  const wordMax = 100;
  let post = "";

  function validateContent(po) {
    po.replace(/[^a-zA-Z\u00C0-\u017F]/g, ""); // Remove punctuation
    return po.length !== 0;
  }

  // Update word count display
  $("#replyInput").on("keyup", (event) => {
    post = $(event.currentTarget).val();
    const words = post.trim().split(/\s+/);
    let wordCount = words.length;
    let remaining = wordMax - wordCount;

    if (post.trim().length === 0) {
      remaining = wordMax;
    }

    $("#words").css("color", remaining <= 0 ? "red" : "white");
    $("#words").html(remaining);
  });

  // Handle send button click
  $("#btn-send").on("click", function () {
    const wordCount = parseInt($("#words").text());
    if (wordCount < 0) {
      alert("You can only type up to 100 words.");
    } else if (wordCount === wordMax) {
      alert("Please enter content before sending");
    } else if (!validateContent(post)) {
      alert("Please enter content worth sending");
    } else {
      sendReply();
    }
  });

  function sendReply() {
    const replyBody = $("#replyInput").val();
    const isAnonymous = $("#flexCheckDefault").is(":checked");
    const username = localStorage.getItem("username");
    const sendId = $("#noteContentContainer").data("send-id");

    $.ajax({
      url: `/user/${username}/reply`,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({
        reply_body: replyBody,
        anonymous: isAnonymous,
        note_id: sendId,
      }),
      success: function () {
        alert("Reply sent successfully!");
        window.location.href = `/user/${username}`;
      },
      error: function (error) {
        console.error("Error sending reply:", error);
      },
    });
  }

  // Fetch user info
  $.ajax({
    url: "/get_user_info",
    type: "GET",
    success: function (response) {
      $("#username").text(response.username);
      localStorage.setItem("username", response.username);

      const storedUsername = localStorage.getItem("username");
      console.log("Stored Username:", storedUsername);

      backToIndex(storedUsername);
    },
    error: function (error) {
      console.log("Error:", error);
    },
  });

  function backToIndex(username) {
    $(".btn-close").on("click", function () {
      window.location.href = `/user/${username}`;
    });
    $(".logo-link").on("click", function () {
      window.location.href = `/user/${username}`;
    });
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
      url: `/api/random_note_by_label?label=${encodeURIComponent(label)}`,
      method: "GET",
      success: function (data) {
        if (data.body) {
          updateNoteContent(data);
        }
      },
      error: function (error) {
        console.error("Error fetching note by label:", error);
        alert("No notes found for this label.");
        const username = localStorage.getItem("username");
        window.location.href = `/user/${username}`;
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

  // Fetch notes based on label or random
  const params = new URLSearchParams(window.location.search);
  const label = params.get("label");
  if (label) {
    fetchNotesByLabel(label);
  } else {
    fetchRandomNote();
  }

  // Fetch next note on button click
  $("#check-next").on("click", function () {
    if (label) {
      fetchNotesByLabel(label);
    } else {
      fetchRandomNote();
    }
  });

  $(document).on("click", "#reply", function () {
    $("#reply-content").hide();
    $("#replyContainer").css("display", "block");
  });

  // Clear content container on close
  $(document).on("click", ".btn-close", function () {
    $("#contentContainer").empty();
  });
});
