/* return to the index when click the btn-close button */
document.querySelector("#close-note").addEventListener("click", function () {
  window.history.back();
});
document
  .querySelector("#close-add-label")
  .addEventListener("click", function () {
    $("#label-section").hide();
  });
/* limit the word count in the text area */
$("#noteInput").focus();
// max words count as 100
var wordMax = 100;
// content inside text input area
var post = "";

function validateContent(po) {
  po.replace(/[^a-zA-Z\u00C0-\u017F]/g, ""); // remove any punctuation
  if (po.length == 0) {
    return false;
  }
  return true;
}
function read_labels() {}

$("#noteInput").on("keyup", (event) => {
  post = $(event.currentTarget).val();
  let words = post.trim().split(/\s+/);
  let wordCount = words.length;
  let remaining = wordMax - wordCount;
  if (post.trim().length === 0) {
    remaining = wordMax;
  }
  if (remaining <= 0) {
    $("#words").css("color", "red");
  } else {
    $("#words").css("color", "white");
  }
  $("#words").html(remaining);
});

/*  hide the label section when the page is loaded */
$("#label-section").hide();

/* alert when you type more than 100 words and cannot click 'next' button */
document.querySelector("#btn-next").addEventListener("click", function () {
  /* need to wait for the cursor leaves the text area and get the count from '#words' */
  let wordCount = parseInt($("#words").text());
  if (wordCount < 0) {
    alert("You can only type up to 100 words.");
  } else if (wordCount == wordMax) {
    alert("Please enter content before sending");
  } else if (!validateContent(post)) {
    alert("Please enter content worth sending");
  } else {
    /* show the label section when the button is clicked */
    $("#label-section").show();
    $("#labelInput").keypress(function (e) {
      if (e.which == 13) {
        e.preventDefault();
        var labelValue = $(this).val().trim();
        if (labelValue && $("#label-list .label").length < 5) {
          var newLabel = $(
            '<div><p class="label"></p><button type="button" class="btn-close" id="close-label" aria-label="Close"></button></div>'
          );
          newLabel.find(".label").text(labelValue);
          $("#label-list").append(newLabel);
          $(this).val("");
        }
      }
    });

    /* when click the close button, remove the label */
    $("#label-list").on("click", ".btn-close", function () {
      $(this).parent().remove();
    });

    /* when the OK! button is clicked, send the labels to the server */
    $("#btn-next2").click(function () {
      // check the number of labels to send
      let childCount = $("#label-list").children().length;
      // no sending if no label were added
      if (childCount == 0) {
        alert("Please add at least one label");
      } else {
        // jump to index after the note is added
        let labelList = [];
        $("#label-list")
          .children()
          .each(function () {
            labelList.push($(this).find(".label").text());
          });
        console.log(labelList);
        alert("You have successfully added a note!");
        window.location.href = "../templates/index.html";
      }
    });
  }
});

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

  // send the note data to the server
});
