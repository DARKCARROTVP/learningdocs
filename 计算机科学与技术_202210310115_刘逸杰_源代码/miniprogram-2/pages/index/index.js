// pages/index/index.js
Page({
  data: {
    unfinishedTasksCount: 0,  // 存储未完成作业的数量
    homeworkTasks: []         // 存储未完成作业的列表
  },

  onLoad: function () {
    // 页面首次加载时获取未完成作业数量
    this.loadTasksData();
  },

  onShow: function () {
    // 页面每次显示时都重新获取未完成作业数量
    this.loadTasksData();
  },

  loadTasksData: function () {
    // 获取保存在本地存储中的任务列表
    const homeworkTasks = wx.getStorageSync('homeworkTasks') || [];
    this.setData({
      homeworkTasks
    });
    this.updateUnfinishedTasksCount();
  },

  updateUnfinishedTasksCount: function () {
    // 计算未完成作业的数量
    const unfinishedCount = this.data.homeworkTasks.filter(task => !task.completed).length;
    this.setData({
      unfinishedTasksCount: unfinishedCount
    });
  },

  // 监听来自任务页面的更新作业数量事件
  bindupdateUnfinishedTasksCount: function (e) {
    // 更新未完成作业的数量
    this.setData({
      unfinishedTasksCount: e.detail
    });
  },

  navigateToTasks: function () {
    wx.navigateTo({
      url: '/pages/tasks/tasks'
    });
  },
  navigateToTimetable: function () {
    wx.navigateTo({
      url: '/pages/timetable/timetable'
    });
  },navigateToExam: function () {
    wx.navigateTo({
      url: '/pages/exam/exam'
    });
  },navigateToChatGPT: function () {
    wx.navigateTo({
      url: '/pages/chatgpt/chatgpt'
    });
  },navigateToScan: function () {
    wx.navigateTo({
      url: '/pages/signin/signin'
    });
  }
});
