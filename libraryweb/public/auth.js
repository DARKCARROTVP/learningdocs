async function register() {
  const name = document.getElementById("name").value;
  const student_id = document.getElementById("student_id").value;
  const email = document.getElementById("email").value;

  const res = await fetch("/api/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, student_id, email })
  });
  const result = await res.json();
  alert(result.message);
  if (res.ok) window.location.href = "login.html";
}

async function login() {
  const student_id = document.getElementById("student_id").value;
  const email_or_pwd = document.getElementById("email").value;

  // 管理员登录逻辑
  if (student_id === "admin" && email_or_pwd === "admin123") {
    localStorage.setItem("admin", "true");
    alert("✅ 管理员登录成功");
    window.location.href = "admin.html";
    return;
  }

  // 读者登录逻辑
  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ student_id, email: email_or_pwd })
  });
  const result = await res.json();
  if (res.ok) {
    localStorage.setItem("student_id", student_id);
    localStorage.setItem("admin", "false");
    alert("✅ 登录成功");
    window.location.href = "index.html";
  } else {
    alert(result.message);
  }
}
