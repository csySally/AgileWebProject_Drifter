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
