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
});
