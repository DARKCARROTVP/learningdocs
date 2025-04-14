(function guard() {
  const path = window.location.pathname;
  const isAdmin = localStorage.getItem("admin") === "true";
  const student_id = localStorage.getItem("student_id");

  if (path.includes("admin") && !isAdmin) {
    alert("请先以管理员身份登录！");
    window.location.href = "login.html";
  }

  if (path.includes("mybooks") && !student_id) {
    alert("请先登录！");
    window.location.href = "login.html";
  }

  if (path.includes("index") && !student_id && !isAdmin) {
    alert("请先登录！");
    window.location.href = "login.html";
  }
})();
