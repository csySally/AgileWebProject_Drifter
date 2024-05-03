// after users open the envelop, can check the note
$(document).ready(function () {
  $("#open").on("click", function (event) {
    $.ajax({
      url: "../templates/check_and_reply.html",
      success: function (html) {
        $("#contentContainer").html(html);
      },
      error: function (error) {
        console.error("Error loading check_and_reply.html:", error);
      },
    });
  });

  // click close note button to return to the reply_note_entry page
  $(document).on("click", "#close-note", function () {
    window.location.href = "../templates/reply_note_entry.html";
  });

  // 事件委托处理关闭按钮
  $(document).on("click", ".btn-close", function () {
    $("#contentContainer").empty(); // 清空内容
  });

  // 处理查看另一条笔记的按钮
  $(document).on("click", "#check-next", function () {
    fetchRandomNote();
  });

  function fetchRandomNote() {
    $.ajax({
      url: "#",
      method: "GET",
      success: function (data) {
        updateNoteContent(data);
      },
      error: function (error) {
        console.error("Error fetching next note:", error);
      },
    });
  }

  $(document).on("click", "#reply", function () {
    // 隐藏查看笔记内容
    $("#reply-content").hide();
    // 显示回复笔记内容
    $("#replyContainer").css("display", "block");
  });
});
