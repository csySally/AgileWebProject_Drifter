// Change the image of user avatar
document.getElementById("userImage").addEventListener("click", function () {
  document.getElementById("imageUpload").click();
});

document.getElementById("imageUpload").addEventListener("change", function () {
  var file = this.files[0];
  if (file) {
    var reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById("userImage").src = e.target.result;
    };
    reader.readAsDataURL(file);
  }
});

document.querySelector("#logout").addEventListener("click", function () {
  var txt;
  var r = confirm("Are you sure you want to log out");
  if (r === true) {
    txt = "You pressed OK!";
    /* logout logic to be added here*/

    window.location.href = "../templates/login.html";
  } else {
    txt = "You pressed Cancel!";
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
});
