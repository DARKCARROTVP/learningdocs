const mongoose = require('mongoose');

const readerSchema = new mongoose.Schema({
  name: String,
  student_id: String,
  email: String,
  borrowed_books: [String]
});

module.exports = mongoose.model('Reader', readerSchema);
