Page({
  data: {
    examInfo: [
      {
        subject: '网络安全与信息加密技术',
        time: '第17周 星期五 08:45-10:20',
        location: '教学3A305	'
      },
      {
        subject: '计算机原理与汇编	', 
        time: '第17周 星期一 13:10-14:45',
        location: '教学2B402'
      },
      {
        subject: '操作系统', 
        time: '第17周 星期二 08:45-10:20',
        location: '教学3A301	'
      },
      {
        subject: '编译原理	',
        time: '第17周 星期二 10:45-12:20',
        location: '教学2B301	'
      },
      {
        subject: '机器学习导论	', 
        time: '未知',
        location: '未知'
      }
    ]
  },

  onLoad: function() {
    // 页面加载时可以添加逻辑来动态获取考试信息
    console.log('Exam page loaded');
  }
});
