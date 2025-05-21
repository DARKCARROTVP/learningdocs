// pages/signin/signin.js
Page({
  data: {
    qrCodeImage: '/images/scan.png',  // 使用固定路径的二维码图像
  },

  onReady: function () {
    // 不再需要生成二维码，因为已通过固定路径展示
  },

  // 扫描二维码
  scanQRCode: function () {
    wx.scanCode({
      //扫码成功回调
      success(res) {
        console.log('扫描结果:', res.result);
        // 跳转到签到成功页面
        wx.navigateTo({
          url: '/pages/signin/success' // 扫描二维码后跳转到签到成功页面
        });
      },
      //扫码失败回调
      fail() {
        wx.showToast({
          title: '扫码失败，请重试',
          icon: 'none'
        });
      }
    });
  },

  navigateToSuccess: function () {
    wx.navigateTo({
      url: '/pages/signin/success' // 直接跳转到签到成功页面
    });
  }
});
