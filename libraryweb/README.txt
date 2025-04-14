📚 电子图书馆系统

本项目是一个基于 Node.js + MongoDB 构建的电子图书馆管理系统，支持读者借阅图书、管理员上传图书、图书查询、借阅统计和数据导出等功能，前后端全部集成，适用于本地或局域网部署。

---

🚀 功能特性

🎓 读者端
- 用户注册 / 登录
- 查看所有图书
- 借阅与归还图书
- 查看个人借阅列表

🛠 管理员端
- 登录管理员后台
- 上传 / 修改 / 删除图书
- 查看借出人学号与姓名
- 查看每本书借阅总次数
- 一键导出借阅数据为 CSV 文件

---

💻 技术栈

- 前端：HTML + JS + 原生 DOM 操作
- 后端：Node.js + Express
- 数据库：MongoDB（使用 mongoose 管理模型）
- 静态托管：Express 静态托管 public/ 页面
- 数据导出：CSV（通过纯字符串拼接导出）

---

📦 项目结构

library-system/
├── app.js                  # 后端入口
├── models/
│   ├── book.js             # 图书模型
│   └── reader.js           # 读者模型
├── public/                 # 前端页面
│   ├── index.html          # 图书馆首页（借阅/搜索）
│   ├── login.html          # 登录页面
│   ├── register.html       # 注册页面
│   ├── mybooks.html        # 读者借书记录
│   ├── admin.html          # 管理员界面
│   ├── auth.js             # 登录/注册逻辑
│   └── auth-guard.js       # 登录跳转保护脚本
└── package.json            # 项目依赖定义

---

🧪 启动与运行

1. 安装依赖

npm install

2. 启动 MongoDB

例如（macOS）：

brew services start mongodb-community@6.0

或手动指定数据目录：

mongod --dbpath ~/mongo-data

3. 启动项目

node app.js

你应看到：

✅ Server running at http://localhost:3000

---

🌐 局域网访问（推荐部署形式）

1. 修改 app.js：

app.listen(3000, '0.0.0.0', () => {
  console.log('✅ Server running...');
});

2. 查询本机局域网 IP：

ifconfig  # 找到如 inet 172.20.10.2

3. 用其他设备浏览器访问：

http://172.20.10.2:3000/index.html

---

📥 导出借阅数据

管理员登录后，点击“📥 导出借阅数据 CSV”按钮，将下载图书借阅信息，包括：

- 书名、作者、ISBN
- 是否借出、借出人学号与姓名
- 借阅总次数

---

🧾 管理员登录方式（默认账号）

- 学号：admin
- 密码：admin123

---

📄 许可证 License

本项目仅用于课程设计/学习目的，不可用于商业用途。
