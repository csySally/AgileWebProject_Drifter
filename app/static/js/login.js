document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("login-form");
  // Listen on form submission events
  loginForm.addEventListener("submit", function (event) {
    // prevent form to submit
    event.preventDefault();
    // get username and password from
    const usn = document.getElementById("username").value;
    const pwd = document.getElementById("password").value;
    console.log(usn, pwd);
    // if (pwd){
    //   return;
    // }
    $.ajax({
      url: "/login",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify({ username: usn, password: pwd }),
      success: function (response) {
        // login successful
        window.location.href = "/index";
      },
      error: function (xhr, status, error) {
        // login failed and show error
        const errorMessage = xhr.responseJSON.error;
        console.log(errorMessage);
        alert(errorMessage);
        // clear password field
        document.getElementById("password").value = "";
      },
    });
  });
});
