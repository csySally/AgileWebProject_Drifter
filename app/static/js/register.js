// validate the form before submitting
function validateForm() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirmPassword").value;

  // username regular expression: 6-12 characters long and contain both letters and numbers
  var usernameRegex = /^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,12}$/;

  // password regular expression: at least 8 characters long and contain at least one lowercase letter, one uppercase letter, and one digit
  var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;

  // check if the username and password meet the requirements
  if (!usernameRegex.test(username)) {
    alert(
      "Username must be 6-12 characters long and contain both letters and numbers."
    );
    return false;
  }

  if (!passwordRegex.test(password)) {
    alert(
      "Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, and one digit."
    );
    return false;
  }

  // check if the password and confirm password match
  if (password !== confirmPassword) {
    alert("Passwords do not match.");
    return false;
  }

  return true;
}
