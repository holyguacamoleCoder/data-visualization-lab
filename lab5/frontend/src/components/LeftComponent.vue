<template>
  <div class="left">
    <div class="headers-title">驾驶行为画像</div>
    <div class="radarAnalyze">
      <div class="title">驾驶行为画像雷达图</div>
      <div class="radar-chart"></div>
    </div>
    <div class="usrAnalyze">
      <div class="title">驾驶用户分析</div>
      <div class="user-list">
        <button v-for="item in waitAnalyze" :key="item">{{item}}
          <span @click="handleSubSelect(item)">-</span>
        </button>
      </div>
      <div class="analyze-btns">
        <button @click="handleAnalyzeRadar">对比分析</button>
        <button>添加Id</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { getRadarData } from '../api/LeftComponent'
export default {
  name: 'LeftComponent',
  data() {
    return {
      waitAnalyze: [172577571, 175202352],
      radarData: null,
      chartInstance: null,
      chartData: {
        indicator: [
          { name: '直行最大速度' },
          { name: '转弯平均速度' },
          { name: '变道次数'},
          { name: '急减速次数'},
          { name: '急加速次数'},
          { name: '直行平均速度'}
        ],
        value: [0, 0, 0, 0, 0, 0]
      }
    }
  },
  mounted() {
    this.initChart()
  },
  computed: {
    ...mapState(['processData', 'hasGotData', 'timeRange']),
  },
  methods: {
    initChart() {
      const echarts = this.$echarts
      this.chartInstance = echarts.init(document.querySelector('.radar-chart'))
      const option = {
        title: {
            // text: '基础雷达图'
        },
        tooltip: {},
        legend: {
            data:[] 
            // ['预算分配（Allocated Budget）', '实际开销（Actual Spending）']
        },
        radar: {
            // shape: 'circle',
            axisName: {
                
                    color: '#111',
                    // backgroundColor: '#999',
                    borderRadius: 3,
                    padding: [3, 5]
                
            },
            axisNameGap: 8,
            indicator: this.chartData.indicator,
            radius: 50
        },
        series: [{
            name: '画像雷达图',
            type: 'radar',
            areaStyle: {},
            symbol: 'circle',
            symbolSize: 4,
            color: '#BDE1D5',
            data: [
                {
                    value: this.chartData.value,
                    name: '画像雷达图'
                }
            ]
        }]
      }//option
      this.chartInstance.setOption(option);
    },
    updateChart() {

    },
    handleSubSelect(id){
      this.waitAnalyze = this.waitAnalyze.filter(item=>item!==id)
    },
    async handleAnalyzeRadar(){
      console.log('refs:',this.$refs.timeline)

      // //将选择列表提交给后端进行分析
      // const params = {
      //   start_time: 1681316252099657,
      //   end_time: 1681316700099673,
      //   ids: this.waitAnalyze
      // }
      const {start_time, end_time} = this.timeRange
      //将选择列表提交给后端进行分析
      const params = {
        start_time,
        end_time,
        ids: this.waitAnalyze
      }
      const {data} = await getRadarData(params)
      this.radarData = data
      // console.log('data', this.radarData)
      const key = this.waitAnalyze[0]
      if(Object.keys(this.radarData) === 0){
        return 
      }
      const item = this.radarData[key].radar_index
      this.chartData.value = [
        item.max_straight_speed,
        item.avg_turn_speed,
        item.lane_change_count,
        item.hard_accel_count,
        item.hard_brake_count,
        item.avg_straight_speed,
      ]
      this.initChart()
    }
  },//method
  watch:{
    hasGotData: {
      handler() {
        this.waitAnalyze = []
        Object.entries(this.processData).forEach(item=>{
          this.waitAnalyze.push(item[0])
        })
        this.initChart()
      },
      deep: true
    }
  }//watch
}
</script>

<style lang="less">
.left {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 0;
  border-radius: 5px;
  height: 460px;
  .headers-title{
    padding-top: 5px;
    border-radius: 5px;
    width: 300px;
    height: 32px;
    font-size: 17px;
    font-weight: bold;
    text-align: center;
    background-color: #A0ACE6;
    color: #fff;
  }
}
.radarAnalyze{
  border-radius: 5px;
  background-color: #fff;
  height: 200px;
  .title{
    position: relative;
    border-radius: 5px;
    width: 100%;
    height: 17px;
    font-size: 12px;
    text-align: left;
    padding-left: 18px;
  }
  .title::before{
    content: '';
    position: absolute;
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 7px;
    background-color: #A0ACE6;
    top: 4px;
    left: 7px;
  }
  .radar-chart {
    height: 163px;
  }
}
.usrAnalyze{
  position: relative;
  border-radius: 5px;
  height: 220px;
  background-color: #fff;
  .title{
    position: relative;
    border-radius: 5px;
    width: 100%;
    height: 17px;
    font-size: 12px;
    text-align: left;
    padding-left: 18px;
  }
  .title::before{
    content: '';
    position: absolute;
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 7px;
    background-color: #A0ACE6;
    top: 4px;
    left: 7px;
  }
  .user-list {
    padding: 5px;
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    button {
      display: block;
      margin-bottom: 5px;
      width: calc(100% / 3 - 10px);
      height: 30px;
      border-radius: 5px;
      background-color: #A0ACE6;
      color: #fff;
      border: 0;
    }
  }
  .analyze-btns{
    position: absolute;
    bottom: 5px;
    left: 25px;
    width: 80%;
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    button {
      display: block;
      margin-bottom: 5px;
      width: calc(100% / 3 - 10px);
      height: 30px;
      background-color: #A0ACE6;
      color: #fff;
      border: 0;
    }
  }
}
</style>
