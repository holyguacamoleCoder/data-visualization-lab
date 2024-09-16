<template>
  <div id="week-view" style="height: 400px;"></div>
</template>

<script>
export default {
  name: 'WeekView',
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      var chart = this.$echarts.init(document.getElementById('week-view'));
      var option = {
        title: {
          text: 'Week View'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['Week1', 'Week2', 'Week3', 'Week4', 'Week5', 'Week6', 'Week7', 'Week8', 'Week9', 'Week10'],
          name: 'Week'
        },
        yAxis: {
          type: 'category',
          data: ['User 1', 'User 2', 'User 3', 'User 4', 'User 5'],
          name: 'Users'
        },
        series: [
          {
            name: 'Progress',
            type: 'scatter',
            symbolSize: function (val) {
              return val[2] * 10; // 控制每个点的大小
            },
            data: [
              [0, 0, 1], [1, 1, 2], [2, 2, 3], [3, 3, 4], [4, 4, 1], // 示例数据
              [5, 0, 1], [6, 1, 2], [7, 2, 3], [8, 3, 4], [9, 4, 1]
            ],
            emphasis: {
              focus: 'series'
            }
          }
        ]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
#week-view {
  width: 100%;
}
</style>
