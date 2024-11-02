<template>
  <div class="bottom">
    <div class="acceleration-change">
      <div class="title">车辆加速度变化</div>
      <div id="acceleration-chart"></div>
      <div class="a-legend">
        <div v-for="item in accelerationLegend" :key="item.id" >
          <div :style="{ 
            backgroundColor:item.color,
            width: '10px',
            height: '10px',
            borderRadius: '3px',
            display: 'inline-block',
            marginLeft: '10px',
            verticalAlign: 'middle'
          }"></div>
          {{ item.name }}
        </div>
      </div>
    </div>
    <div class="speed-ratio">
      <div class="title">车辆速度比例</div>
      <div id="speed-chart"></div>
      <div class="sd-legend">
        <div v-for="item in speedDistributionLegend" :key="item.id" class="sd-legend-item">
          <div :style="{ 
            backgroundColor:item.color,
            width: '10px',
            height: '10px',
            borderRadius: '3px',
            display: 'inline-block',
            marginLeft: '10px',
            verticalAlign: 'middle'
          }"></div>
          {{ item.name }}
        </div>
      </div>
    </div>
    <div class="speed-lane-direction">
      <div class="title">速度-变道-朝向变化</div>
      <div id="line-chart"></div>
      <div class="so-legend">
        <div v-for="item in speedOrientLegend" :key="item.id" >
          <div :style="{ 
            backgroundColor:item.color,
            width: '10px',
            height: '10px',
            borderRadius: '3px',
            display: 'inline-block',
            marginLeft: '10px',
            verticalAlign: 'middle'
          }" :class="{'ori-legend-item': item.id === 0}"></div>
          {{ item.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'BottomComponent',
  data() {
    return {
      accelerationData: [],
      speedDistributionData: [],
      speedOrientationData: [],
      accelerationLegend: [
        { id: 0, name: '-6~-3m/s²', color: '#0D569E'},
        { id: 1, name: '-3~-0m/s²', color: '#209FFE' },
        { id: 2, name: '0~3m/s²', color: '#FDE040' },
        { id: 3, name: '3~6m/s²', color: '#FF6928' },
      ],
      speedDistributionLegend: [
        { id: 0, name: '0~11m/s', color: '#CAEBBF'},
        { id: 1, name: '11~14m/s', color: '#ADD9AE' },
        { id: 2, name: '14~17m/s', color: '#7DC0A1' },
        { id: 3, name: '>17m/s', color: '#47A2A8' },
      ],
      speedOrientLegend: [
        { id: 0, name: '车辆朝向差值', color: '#F1974E'},
        { id: 1, name: '车辆速度大小', color: '#A1D197' },
        { id: 2, name: '车辆静止', color: '#EAE6E7' },
      ]
    }
  },
  computed: {
    ...mapState(['processData', 'hasGotData', 'timeRange']),
  },
  mounted() {
    console.log('mount')
  },
  methods: {
    renderAccelerationChart() {
      const d3 = this.$d3
      const width = 500
      const height = 200
      const everyHeight = 30
      const svg = d3.select('#acceleration-chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
      const margin = { top: 20, right: 12, bottom: 30, left: 12 }
      const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`)
      const timelineX = d3.scaleUtc()
        .domain([new Date(this.timeRange.start_time), new Date(this.timeRange.end_time )])
        .range([0, width - margin.left - margin.right])
      const accelerationY = d3.scaleLinear()
        .domain([0, 3])
        .range([0, everyHeight / 2])
      // 遍历每个id物体
      // this.accelerationData.length = 1
      this.accelerationData.forEach((item, index) => {
        const id = item.id
        const data = item.data
        const ig = g.append('g')
          .attr('transform', `translate(${0}, ${index * (everyHeight + 5)})`)
          .attr('class', 'every-id')
        
        //定义面积生成器
        // const area = d3.area()
        // .x(dd => timelineX(new Date(dd.time)))
        // .y1(accelerationY(0))
        // .y0(dd => accelerationY(dd.acceleration))
        
        
        ig.append('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', width - margin.left - margin.right + 4)
        .attr('height', everyHeight)
        .attr('fill', '#97E3FF')
        .attr('stroke-width', 1)
        .attr('stroke', '#2E76A7')
        .on('mouseover', function(){
          d3.select('#line-chart').selectAll('rect').attr('opacity', 0.5)
          d3.select('#speed-chart').selectAll('rect').attr('opacity', 0.5)
          d3.select('#acceleration-chart').selectAll('rect').attr('opacity', 0.5)
        })
        .on('mouseout', function(){
          d3.select('#line-chart').selectAll('rect').attr('opacity', 1)
          d3.select('#speed-chart').selectAll('rect').attr('opacity', 1)
          d3.select('#acceleration-chart').selectAll('rect').attr('opacity', 1)
        })

        // 添加时间轴

        ig.append('line')
        .attr('x1', 0)
        .attr('y1', everyHeight / 2)
        .attr('x2', width - margin.left - margin.right)
        .attr('y2', everyHeight / 2)
        .attr('stroke', '#2E76A7')
        .attr('stroke-width', 1)

        // 添加id
        ig.append('text')
        .text(id)
        .attr('x', 0)
        .attr('y', (1 / 2) * everyHeight - 5)
        .attr('fill', 'black')
        .attr('font-size', 10)


        ig.selectAll(`.rect-data${index}`)
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => timelineX(new Date(d.time_meas)))
        .attr('y', d => d.acceleration >= 0 ? everyHeight / 2 - accelerationY(d.acceleration) : everyHeight / 2)
        .attr('width', 2)
        .attr('height', d => accelerationY(Math.abs(d.acceleration)))
        .attr('fill', d => this.accelerationLegend[d.bin].color)
        .on('mouseover', function(){
          d3.select(this).attr('opacity', 0.5)
        })
        .on('mouseout', function(){
          d3.select(this).attr('opacity', 1)
        })

      })
    },
    renderSpeedDistributeChart() {
      const d3 = this.$d3
      const width = 200
      const height = 200
      const everyHeight = 30
      const svg = d3.select('#speed-chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
      const margin = { top: 20, right: 9, bottom: 30, left: 7 }
      const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`)

      const distributionX = d3.scaleLinear()
        .domain([0, 100])
        .range([0, width - margin.left - margin.right])
      
      // 创建 X 轴
      const scaleX = d3.scaleLinear()
      .domain([0, 1])
      .range([0, width - margin.left - margin.right - 2])
      const xAxis = d3.axisTop(scaleX)
      .ticks(3)  // 设置刻度数量为 3
      .tickValues([0, 0.5, 1])  // 指定刻度值
      .tickFormat(d3.format('.0%'));  // 格式化刻度值为百分比

      // 添加 X 轴到 SVG
      g.append('g')
      .attr('class', 'axis')
      .attr('transform', `translate(${1}, ${0})`)
      .call(xAxis)
      d3.selectAll('.tick text').attr('font-size', '7px')

      // 遍历每个id物体
      // this.accelerationData.length = 1
      this.speedDistributionData.forEach((item, index) => {
        // const id = item.id
        const data = item.data
        const ig = g.append('g')
          .attr('transform', `translate(${0}, ${index * (everyHeight + 1)})`)
          .attr('class', 'every-car')
        let currentWidth = 0
        let nextWidth = 0
        ig.selectAll('.distribution-rect')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', (d, i) => {
          if(i === 0){
            nextWidth = distributionX(d.percentage)
            return currentWidth
          }
          else{
            currentWidth = nextWidth
            nextWidth = distributionX(d.percentage) + currentWidth
            return currentWidth
          }
        })
        .attr('y', 0)
        .attr('rx', 2)
        .attr('width', d => distributionX(d.percentage))
        .attr('height', everyHeight)
        .attr('fill', d => this.speedDistributionLegend[d.bin].color)
        .on('mouseover', function(){
          d3.select('#line-chart').selectAll('rect').attr('opacity', 0.5)
          d3.select('#speed-chart').selectAll('rect').attr('opacity', 0.5)
          d3.select('#acceleration-chart').selectAll('rect').attr('opacity', 0.5)
        })
        .on('mouseout', function(){
          d3.select('#line-chart').selectAll('rect').attr('opacity', 1)
          d3.select('#speed-chart').selectAll('rect').attr('opacity', 1)
          d3.select('#acceleration-chart').selectAll('rect').attr('opacity', 1)
        })
        
      })
    },
    renderSeepOrientedChart() {
      const d3 = this.$d3
      const width = 580
      const height = 200
      const everyHeight = 30
      const svg = d3.select('#line-chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
      const margin = { top: 20, right: 12, bottom: 30, left: 12 }
      const g = svg.append('g').attr('transform', `translate(${margin.left}, ${margin.top})`)
      const timelineX = d3.scaleUtc()
        .domain([new Date(this.timeRange.start_time), new Date(this.timeRange.end_time)])
        .range([0, width - margin.left - margin.right])
      const orientationY = d3.scaleLinear()
        .domain([0, Math.PI / 2])
        .range([0, everyHeight])
      
      // 遍历每个id物体
      // this.accelerationData.length = 1
      this.speedOrientationData.forEach((item, index) => {
        // const id = item.id
        const s_data = item.s_data
        const o_data = item.o_data
        const ig = g.append('g')
          .attr('transform', `translate(${0}, ${index * (everyHeight + 5)})`)
          .attr('class', 'every-id')
         //-----------------速度视图部分-----------------
         const colorScale = d3.scaleLinear()
        .domain([0, d3.max(s_data, d => d.velocity)])
        .range(['#F6FBF4', '#4EB063'])
        // 添加线性渐变
        const gradient = ig.append('defs').append('linearGradient')
        .attr('id', `gradient-${index}`)
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '0%')
        gradient.append('stop')
        .attr('offset', '0%')
        // 添加渐变颜色停止点
        s_data.forEach((item, index) => {
          gradient.append('stop')
          .attr('offset', `${index / (s_data.length - 1) * 100}%`)
          .attr('stop-color', colorScale(item.velocity))
        })
        //绘制矩形
        ig.append('rect')
        .attr('class', 'bar')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', width)
        .attr('height', everyHeight)
        .style('fill', `url(#gradient-${index})`)
        .on('mouseover', function(){
          d3.select('#line-chart').selectAll('rect').attr('opacity', 0.5)
          d3.select('#speed-chart').selectAll('rect').attr('opacity', 0.5)
          d3.select('#acceleration-chart').selectAll('rect').attr('opacity', 0.5)
        })
        .on('mouseout', function(){
          d3.select('#line-chart').selectAll('rect').attr('opacity', 1)
          d3.select('#speed-chart').selectAll('rect').attr('opacity', 1)
          d3.select('#acceleration-chart').selectAll('rect').attr('opacity', 1)
        })
        // console.log('s_data')
        //--------------车头朝向部分--------------------
        
        ig.append('path')
        .datum(o_data)
        .attr('fill', 'none')
        .attr('stroke', '#F3AC73')
        .attr('stroke-width', 1)
        .attr('d', d3.line()
          .x(d => {
            // console.log('d', d)
            return timelineX(new Date(d.time_meas))
          })
          .y(d => orientationY(Math.abs(d.orientation_diff)) + 1)
        )
       
      })
    },
    clearData(){
      this.accelerationData = []
      this.speedDistributionData = []
      this.speedOrientationData = []
      return 1
    }
  },//methods
  watch:{
    hasGotData: {
      async handler() {
        const result = await this.clearData()
        console.log('res', result)
        console.log('hsadGotData', this.accelerationData)
        Object.entries(this.processData).forEach(item=>{
          this.accelerationData.push({
            id:item[0],
            data:item[1].acceleration_over_time
          })
          this.speedDistributionData.push({
            id:item[0],
            data:item[1].speeds_distribution
          })
          this.speedOrientationData.push({
            id:item[0],
            s_data:item[1].speed_over_time,
            o_data:item[1].orientation_diff
          })
          console.log('item', item[0])
        })
        this.$d3.select('#acceleration-chart').selectAll('*').remove()
        this.$d3.select('#speed-chart').selectAll('*').remove()
        this.$d3.select('#line-chart').selectAll('*').remove()
        this.renderAccelerationChart()
        this.renderSpeedDistributeChart()
        this.renderSeepOrientedChart()
      },
      deep: true
    }
  }
}
</script>

<style lang="less">
.bottom {
  display: grid;
  grid-template-columns: repeat(3, 300px);
  gap: 10px;
}

.acceleration-change, .speed-ratio, .speed-lane-direction{
  background-color: #fff;
  border-radius: 5px;
  height: 237px;
  .title{
    position: relative;
    margin-top: 5px;
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
  #acceleration-chart, #line-chart{
    width: 100%;
    height: 190px;
  }
  #speed-chart{
    width: 100%;
    height: 180px;
  }
}
.a-legend{
  display: flex;
  flex-direction: row;
  font-size: 9px;
  font-weight: 600;
}
.sd-legend{
  display: flex;
  width: 200px;
  margin: 0 10px;
  flex-direction: row;
  font-size: 7px;
  font-weight: 600;
  flex-wrap: wrap;
  .sd-legend-item{
    margin-right: 20px;
    margin-top: 4px;
    width: calc((100% - 10px) / 3);
  }
}
.speed-lane-direction{
  position: relative;
  .so-legend{
    position: absolute;
    bottom: 20px;
    right: 0;
    width: 100px;
    height: 50px;
    font-size: 9px;
    font-weight: 600;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    .ori-legend-item::before{
        content: '';
        position: absolute;
        top: -8px;
        left: -8px;
        width: 30px;
        height: 30px;
        z-index: 100;
        background: url('../assets/img/legend-ori.png') no-repeat;
        background-size: contain;
        background-position: center;
      }
    
  }
}

</style>
