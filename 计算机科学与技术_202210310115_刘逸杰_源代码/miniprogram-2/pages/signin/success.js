// pages/signin/success.js
Page({
  data: {},

  // 返回首页
  goBack: function () {
    wx.navigateTo({
      url: '/pages/index/index' // 直接跳转到签到成功页面
    });
  }
});
