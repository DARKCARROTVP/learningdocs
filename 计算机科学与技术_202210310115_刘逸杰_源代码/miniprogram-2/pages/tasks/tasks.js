// pages/tasks/tasks.js
Page({
  data: {
    newHomework: '',      // 新作业输入框的内容
    homeworkTasks: []     // 存储未完成的作业
  },

  // 输入框内容变化（作业）
  onHomeworkInput: function (e) {
    this.setData({
      newHomework: e.detail.value
    });
  },

  // 添加未完成作业
  addHomework: function () {
    const newHomework = this.data.newHomework.trim();
    if (newHomework) {
      // 将新作业添加到 homeworkTasks 数组
      const updatedHomeworkTasks = [...this.data.homeworkTasks, newHomework];
      
      // 更新 homeworkTasks 数据源
      this.setData({
        homeworkTasks: updatedHomeworkTasks,
        newHomework: ''  // 清空输入框
      });

      // 保存作业到本地存储
      wx.setStorageSync('homeworkTasks', updatedHomeworkTasks);
    } else {
      wx.showToast({
        title: '请输入作业内容',
        icon: 'none'
      });
    }
  },

  // 删除作业
  deleteHomework: function (e) {
    const index = e.currentTarget.dataset.index; // 获取作业的索引
    const updatedHomeworkTasks = this.data.homeworkTasks.filter((_, i) => i !== index);
    
    // 更新 homeworkTasks 数据源
    this.setData({
      homeworkTasks: updatedHomeworkTasks
    });

    // 保存删除后的作业列表到本地存储
    wx.setStorageSync('homeworkTasks', updatedHomeworkTasks);

    // 通知父页面更新作业数量
    this.triggerEvent('updateUnfinishedTasksCount', updatedHomeworkTasks.length);  // 使用 triggerEvent
  },

  // 页面加载时获取存储的任务列表
  onLoad: function () {
    const homeworkTasks = wx.getStorageSync('homeworkTasks') || [];
    this.setData({
      homeworkTasks
    });
  },

  // 页面卸载时将数据保存到本地存储
  onUnload: function () {
    wx.setStorageSync('homeworkTasks', this.data.homeworkTasks);
  }
});
