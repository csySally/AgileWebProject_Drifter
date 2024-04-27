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

/* alert when you type more than 100 words and cannot click 'next' button */
document.querySelector("#btn-next").addEventListener("click", function () {
  /* need to wait for the cursor leaves the text area and get the count from '#words' */
  let wordCount = parseInt($("#words").text());
  console.log(wordCount);
  if (wordCount < 0) {
    alert("You can only type up to 60 words.");
  } else {
    window.location.href = "../templates/add_tag.html";
  }
});
