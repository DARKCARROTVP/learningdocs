Page({
  data: {
    selectedDay: '',
    courses: [], 
    courseSchedule: {
      星期一: [
        { time: '8:20 - 9:55', course: '编译原理' },
        { time: '10:00 - 11:50', course: '计算机原理与汇编' },
        { time: '13:10 - 14:45', course: '无' },
        { time: '15:05 - 16:40', course: '无' }
      ],
      星期二: [
        { time: '8:20 - 9:55', course: '无' },
        { time: '10:00 - 11:50', course: '计算机原理与汇编' },
        { time: '13:10 - 14:45', course: '计算机原理与汇编实验' },
        { time: '15:05 - 16:40', course: '操作系统实验' }
      ],
      星期三: [
        { time: '8:20 - 9:55', course: '网络安全与信息加密技术' },
        { time: '10:00 - 11:50', course: '无' },
        { time: '13:10 - 14:45', course: '机器学习导论' },
        { time: '15:05 - 16:40', course: '无' }
      ],
      星期四: [
        { time: '8:20 - 9:55', course: '机器学习导论' },
        { time: '10:00 - 11:50', course: '操作系统' },
        { time: '13:10 - 14:45', course: '无' },
        { time: '15:05 - 16:40', course: '网络安全与信息加密技术' }
      ],
      星期五: [
        { time: '8:20 - 9:55', course: '无' },
        { time: '10:00 - 11:50', course: '计算机伦理学' },
        { time: '13:10 - 14:45', course: '编译原理' },
        { time: '15:05 - 16:40', course: '操作系统' }
      ],
      星期六: [
        { time: '8:20 - 9:55', course: '企业事务实训' },
        { time: '10:00 - 11:50', course: '企业事务实训' },
        { time: '13:10 - 14:45', course: '无' },
        { time: '15:05 - 16:40', course: '无' }
      ],
      星期天: [
        { time: '8:20 - 9:55', course: '无' },
        { time: '10:00 - 11:50', course: '无' },
        { time: '13:10 - 14:45', course: '无' },
        { time: '15:05 - 16:40', course: '无' }
      ]
    },
  },

  showCourses: function(e) {
    const day = e.currentTarget.dataset.day;
    this.setData({
      selectedDay: day,
      courses: this.data.courseSchedule[day]
    });
  }
});
