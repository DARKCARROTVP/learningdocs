const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const Book = require('./models/book');
const Reader = require('./models/reader');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static('public'));

mongoose.connect('mongodb://127.0.0.1:27017/libraryDB');

// 图书接口
app.get('/api/books', async (req, res) => {
  const books = await Book.find();
  const readers = await Reader.find({}, { student_id: 1, name: 1 });

  const idToName = {};
  readers.forEach(reader => {
    idToName[reader.student_id] = reader.name;
  });

  const enrichedBooks = books.map(book => ({
    ...book.toObject(),
    borrower_name: idToName[book.borrowed_by] || null 
  }));

  res.json(enrichedBooks);
});


app.post('/api/borrow', async (req, res) => {
  const { isbn, student_id } = req.body;
  const book = await Book.findOne({ isbn });

  if (!book || !book.available) {
    return res.status(400).json({ message: '图书不可借' });
  }

  await Book.updateOne(
    { isbn },
    {
      available: false,
      borrowed_by: student_id,
      $inc: { borrow_count: 1 }
    }
  );

  await Reader.updateOne(
    { student_id },
    { $addToSet: { borrowed_books: isbn } }
  );

  res.json({ message: '借书成功' });
});


app.post('/api/return', async (req, res) => {
  const { isbn, student_id } = req.body;
  const book = await Book.findOne({ isbn });
  if (!book || book.available || book.borrowed_by !== student_id) {
    return res.status(400).json({ message: '不能归还此书' });
  }

  await Book.updateOne({ isbn }, { available: true, borrowed_by: null });
  await Reader.updateOne({ student_id }, { $pull: { borrowed_books: isbn } });
  res.json({ message: '还书成功' });
});

// 用户注册登录
app.post('/api/register', async (req, res) => {
  const { name, student_id, email } = req.body;
  const exists = await Reader.findOne({ student_id });
  if (exists) return res.status(400).json({ message: "学号已注册" });
  await Reader.create({ name, student_id, email, borrowed_books: [] });
  res.json({ message: "注册成功" });
});

app.post('/api/login', async (req, res) => {
  const { student_id, email } = req.body;
  const reader = await Reader.findOne({ student_id, email });
  if (!reader) return res.status(400).json({ message: "学号或邮箱错误" });
  res.json({ message: "登录成功" });
});

// 我的借书列表
app.get('/api/mybooks/:student_id', async (req, res) => {
  const { student_id } = req.params;
  const reader = await Reader.findOne({ student_id });
  if (!reader) return res.status(404).json({ message: "找不到读者" });
  const books = await Book.find({ isbn: { $in: reader.borrowed_books } });
  res.json(books);
});

// 管理图书：上传、删除、修改
app.post('/api/books', async (req, res) => {
  const { title, author, isbn, category } = req.body;
  const exists = await Book.findOne({ isbn });
  if (exists) return res.status(400).json({ message: "ISBN 已存在" });
  await Book.create({ title, author, isbn, category, available: true, borrowed_by: null });
  res.json({ message: "图书上传成功" });
});

app.delete('/api/books/:isbn', async (req, res) => {
  const { isbn } = req.params;
  await Book.deleteOne({ isbn });
  res.json({ message: "图书已删除" });
});

app.put('/api/books/:isbn', async (req, res) => {
  const { isbn } = req.params;
  const { field, value } = req.body;
  const update = {};
  update[field] = value;
  await Book.updateOne({ isbn }, { $set: update });
  res.json({ message: "图书信息已更新" });
});

app.get('/api/export', async (req, res) => {
  const books = await Book.find();
  const readers = await Reader.find({}, { student_id: 1, name: 1 });

  const map = {};
  readers.forEach(r => map[r.student_id] = r.name);

  let csv = '书名,作者,ISBN,是否可借,借出人学号,借出人姓名,借阅次数\n';
  books.forEach(b => {
    csv += `${b.title},${b.author},${b.isbn},${b.available ? '是' : '否'},${b.borrowed_by || ''},${map[b.borrowed_by] || ''},${b.borrow_count || 0}\n`;
  });

  res.setHeader('Content-Type', 'text/csv; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename=library_export.csv');
  res.send('\uFEFF' + csv); 
});

app.listen(3000, '0.0.0.0', () => {
  console.log('✅ Server running at http://172.20.10.2:3000');
});

