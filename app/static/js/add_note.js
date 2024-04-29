/* return to the index when click the btn-close button */
document.querySelector(".btn-close").addEventListener("click", function () {
  window.location.href = "../templates/index.html";
});

/* limit the word count in the text area */
$("#noteInput").focus();

$("#noteInput").on("keyup", (event) => {
  let post = $(event.currentTarget).val();
  let words = post.trim().split(/\s+/);
  let wordCount = words.length;
  let remaining = 100 - wordCount;
  if (post.trim().length === 0) {
    remaining = 100;
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
  console.log(wordCount);
  if (wordCount < 0) {
    alert("You can only type up to 60 words.");
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
      // ...

      // jump to index after the note is added
      alert("You have successfully added a note!");
      window.location.href = "../templates/index.html";
    });
  }
});
