<template>
  <div id="portrait-view" style="display: flex; justify-content: space-around; height: 300px;">
    <div id="radial-chart1" style="width: 30%;"></div>
    <div id="radial-chart2" style="width: 30%;"></div>
    <div id="radial-chart3" style="width: 30%;"></div>
  </div>
</template>

<script>
export default {
  name: 'PortraitView',
  mounted() {
    this.initRadialChart('radial-chart1');
    this.initRadialChart('radial-chart2');
    this.initRadialChart('radial-chart3');
  },
  methods: {
    initRadialChart(id) {
      var chart = this.$echarts.init(document.getElementById(id));
      var option = {
        series: [
          {
            type: 'pie',
            radius: ['40%', '70%'],
            label: {
              show: false
            },
            data: [
              { value: 40, name: 'Part 1' },
              { value: 60, name: 'Part 2' }
            ]
          }
        ]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
#portrait-view {
  width: 100%;
}
</style>
