const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  title: String,
  author: String,
  isbn: String,
  category: String,
  available: Boolean,
  borrowed_by: String,
  borrow_count: { type: Number, default: 0 }
});

module.exports = mongoose.model('Book', bookSchema);
