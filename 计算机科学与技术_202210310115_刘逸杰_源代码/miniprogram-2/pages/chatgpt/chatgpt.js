Page({
  data: {
    inputMessage: '',
    messages: [],
    scrollIntoView: ''
  },

  handleInput(event) {
    this.setData({
      inputMessage: event.detail.value
    });
  },

  async sendMessage() {
    const message = this.data.inputMessage;

    if (!message) {
      return;
    }

    const response = await wx.request({
      url: 'https://api.chatanywhere.com.cn/v1/chat/completions',
      method: 'POST',
      data: {
        "model": "gpt-3.5-turbo",
        "messages": [{
          "role": "user",
          "content": message
        }]
      },
      header: {
        'Authorization': 'Bearer sk-OKPZ0LZ4CTvRE0IfYfPd94Z5ul3zpGSbKdzadr7U5SPTg8jX',
        'Content-Type': 'application/json'
      },
      success: (res) => {
        const reply = res.data.choices[0].message.content;

        this.setData({
          inputMessage: '',
          messages: [...this.data.messages, 
          { content: message, type: 'user', alignment: 'right'},
          { content: reply, type: 'bot', alignment: 'left' },],
          scrollIntoView: 'msg-' + (this.data.messages.length - 1)
        });
      },
      fail: (error) => {
        console.error(error);
      }
    });
  }
});