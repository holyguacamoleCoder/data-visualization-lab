<template>
  <div id="scatter-chart" style="height: 300px;"></div>
</template>

<script>
export default {
  name: 'ScatterView',
  mounted() {
    this.initChart();
  },
  methods: {
    initChart() {
      var chart = this.$echarts.init(document.getElementById('scatter-chart'));
      var option = {
        xAxis: {},
        yAxis: {},
        series: [
          {
            symbolSize: 20,
            data: [
              [10, 8], [15, 11], [8, 5], // Cluster 1
              [20, 10], [21, 15], [23, 18], // Cluster 2
              [30, 22], [28, 24], [27, 25] // Cluster 3
            ],
            type: 'scatter'
          }
        ]
      };
      chart.setOption(option);
    }
  }
};
</script>

<style scoped>
#scatter-chart {
  width: 100%;
}
</style>
