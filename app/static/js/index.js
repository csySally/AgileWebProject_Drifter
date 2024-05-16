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

    var formData = new FormData();
    formData.append("image", file);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload_image", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
        console.log("Image uploaded successfully");
      }
    };
    xhr.send(formData);
  }
});

document.querySelector("#logout").addEventListener("click", function () {
  var r = confirm("Are you sure you want to log out");
  if (r === true) {
    $.ajax({
      type: "POST",
      url: "/logout",
      success: function(response) {
          // show response
          console.log(response);
          alert("log out successful");
          window.location.href = "/";
      },
      error: function(xhr, status, error) {
          // show error if failed to logout
          console.log(xhr, status, error);
          console.log("Error: " + error);
          alert(status);
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
});
