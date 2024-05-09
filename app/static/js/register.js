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

document.addEventListener("DOMContentLoaded", function () {
  var registerForm = document.getElementById("register-form");
  registerForm.addEventListener("submit", function (event) {
    event.preventDefault(); // 阻止表单默认提交

    if (!validateForm()) {
      return false; // 如果客户端验证失败，停止执行
    }

    var data = {
      username: document.getElementById("username").value,
      password: document.getElementById("password").value,
      confirmPassword: document.getElementById("confirmPassword").value,
    };

    fetch("/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json", // 确保服务器知道我们期望的响应类型
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          window.location.href = "/login"; // 如果注册成功，跳转到登录页
        } else {
          alert(data.message); // 显示错误消息
        }
      })
      .catch((error) => console.error("Error:", error));
  });
});
