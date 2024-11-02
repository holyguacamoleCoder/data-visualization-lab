<template>
  <div id="timeline-chart"></div>
</template>

<script>
import { getTimestampRange } from '@/api/TimelineSlider'
import { mapActions } from 'vuex'
export default {
  name: 'TimelineSlider',
  data() {
    return {
      chart: null,
      selTime1: null,
      selTime2: null,
      min_timestamp: 0,
      max_timestamp: 0,
      renderData: [],
    }
  },
  created(){
  },
  async mounted(){
    const {data} = await getTimestampRange()
    // console.log(data)
    this.max_timestamp = data.max_timestamp
    this.min_timestamp = data.min_timestamp
    this.renderData = []
    this.generateTimeData(250)
    this.renderTimeline()
  },
  methods:{
    ...mapActions(['toggleTimeRange']),
    generateTimeData(numPoints){
      const maxTimestamp = this.max_timestamp
      const minTimestamp = this.min_timestamp
      const timestampStep = (maxTimestamp - minTimestamp) / (numPoints - 1);
      console.log(minTimestamp)
      console.log(new Date(minTimestamp))
      console.log(new Date(minTimestamp).getTime())
      for (let i = 0; i < numPoints; i++) {
        const time = minTimestamp + i * timestampStep;
        const value = Math.random() * 30;
        this.renderData.push({ time: new Date(time / 1000), value: value });
      }
    },
    renderTimeline(){
      const data = this.renderData
      const d3 = this.$d3
      // 设置SVG的尺寸
      const width = 700
      const height = 90
      const margin = { top: 35, right: 5, bottom: 30, left: 5 }
      const chartWidth = width - margin.left - margin.right
      const chartHeight = height - margin.top - margin.bottom
      const handleWidth = 4
      // 创建SVG元素
      const svg = d3
        .select('#timeline-chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`)
      // console.log('svg', svg)
      // 时间轴比例尺
      const xScale = d3
        .scaleTime()
        .domain(d3.extent(data, (d) => d.time))
        .range([0, chartWidth])

      // 值比例尺
      const yScale = d3
        .scaleLinear()
        .domain([0, 30]) // 固定的最大值
        .range([chartHeight, 0])

      // 添加X轴
      // const xAxis = d3.axisBottom(xScale)
      // svg
      //   .append('g')
      //   .attr('transform', `translate(0, ${chartHeight})`)
      //   .call(xAxis)

      // // 添加Y轴
      // const yAxis = d3.axisLeft(yScale);
      // svg.append('g')
      //   .call(yAxis);

      // 添加柱状图
      const barWidth = chartWidth / data.length
      data.forEach((d) => {
        // 主柱子
        svg
          .append('rect')
          .attr('class', 'bar')
          .attr('x', xScale(d.time) - barWidth / 2)
          .attr('y', yScale(d.value))
          .attr('width', barWidth)
          .attr('height', chartHeight - yScale(d.value))
          .attr('fill', '#AAFAA9')

        // 补充柱子
        svg
          .append('rect')
          .attr('class', 'bar-complement')
          .attr('x', xScale(d.time) - barWidth / 2)
          .attr('y', 0)
          .attr('width', barWidth)
          .attr('height', yScale(d.value))
          .attr('fill', '#F39695')
      })

      // 添加时间轴滑块
      const slider = svg
        .append('g')
        .attr('class', 'slider')
        .attr('transform', `translate(0, ${chartHeight + 10})`)
      const handle1Offset = - 15
      const handle2Offset = -5
      const handle1 = slider
        .append('line')
        .attr('class', 'vertical-line')
        .attr('x1', 0)
        .attr('y1', -chartHeight + handle1Offset)
        .attr('x2', 0)
        .attr('y2', -10)
        .attr('stroke-width', handleWidth)
        .attr('stroke', '#A0ACE6')

      const handle2 = slider
        .append('line')
        .attr('class', 'vertical-line')
        .attr('x1', 0)
        .attr('y1', -chartHeight - 10)
        .attr('x2', 0)
        .attr('y2', handle2Offset)
        .attr('stroke-width', handleWidth)
        .attr('stroke', '#A0ACE6')

      const label1Offset = handle1Offset - 5
      const label2Offset = handle2Offset + 10
      const label1 = slider
        .append('text')
        .attr('class', 'label')
        .attr('y', -chartHeight + label1Offset)
        .attr('font-size', '9px')

      const label2 = slider
        .append('text')
        .attr('class', 'label')
        .attr('x', '-150px')
        .attr('y', label2Offset)
        .attr('font-size', '9px')


      const triUpOffsetX = chartWidth
      const triUpOffsetY = 32
      const triDownOffsetX = 0
      const triDownOffsetY = - chartHeight - 4
      const triangleUp = slider
        .append('polygon')
        .attr('class', 'triangle-up')
        .attr('points', '0,-40 5,-35 -5,-35')
        .attr('fill', '#A0ACE6')
        .attr('transform', `translate(${triUpOffsetX}, ${triUpOffsetY})`)

      const triangleDown = slider
        .append('polygon')
        .attr('class', 'triangle-down')
        .attr('points', '0,-10 5,-15 -5,-15')
        .attr('fill', '#A0ACE6')
      .attr('transform', `translate(${triDownOffsetX}, ${triDownOffsetY})`)

      const mask = svg
        .append('rect')
        .attr('class', 'mask')
        .attr('y', 0)
        .attr('height', chartHeight)
        .attr('fill', 'rgba(160,172,230, 0.6)')

      const drag = d3
        .drag()
        .on('start', function () {
          d3.event.sourceEvent.stopPropagation() // 阻止默认行为
        })
        .on('start drag', function (event) {
          // console.log('dragging')
          const x = Math.max(0, Math.min(chartWidth, event.x)) // 确保滑块在有效范围内
          const date = xScale.invert(x)
          d3.select(this).attr('x1', x).attr('x2', x)
          const label = d3.select(this.parentNode).select('.label')
          label.attr('x', x).text(d3.timeFormat('%Y-%m-%d %H:%M')(date))
          updateChart(date, this === handle1 ? 'start' : 'end')
        })

      handle1.call(drag)
      handle2.call(drag)

      // 初始位置
      const initialStart = xScale.domain()[0]
      const initialEnd = xScale.domain()[1]
      handle1.attr('x1', xScale(initialStart)).attr('x2', xScale(initialStart))
      handle2.attr('x1', xScale(initialEnd)).attr('x2', xScale(initialEnd))
      label1
        .attr('x', xScale(initialStart))
        .text(d3.timeFormat('%Y-%m-%d %H:%M')(initialStart))
      label2
        .attr('x', xScale(initialEnd) - 50)
        .text(d3.timeFormat('%Y-%m-%d %H:%M')(initialEnd))
      // updateLabel(handle1, xScale(initialStart), initialStart)
      // updateLabel(handle2, xScale(initialEnd), initialEnd)
      triangleUp.attr('transform', `translate(${xScale(initialEnd)}, ${triUpOffsetY})`)
      triangleDown.attr('transform', `translate(${xScale(initialStart)}, ${triDownOffsetY})`)
      mask
        .attr('x', xScale(initialStart))
        .attr('width', xScale(initialEnd) - xScale(initialStart))
      // function updateLabel(handle, x, date) {
      //   const labelGroup = handle === handle1 ? label1 : label2
      //   const labelText = d3.timeFormat('%Y-%m-%d %H:%M')(date)
      //   const text = labelGroup
      //     .select('text')
      //     .text(labelText)
      //     .attr('x', x)
      //     .attr('y', -chartHeight - 30)

      //   const bbox = text.node().getBBox()
      //   labelGroup
      //     .select('rect')
      //     .attr('x', x - bbox.width / 2)
      //     .attr('y', -chartHeight - 30 - bbox.height / 2)
      //     .attr('width', bbox.width)
      //     .attr('height', bbox.height)
      //     .attr('fill', 'red')
      //     .attr('rx', 5) // 圆角半径
      // }
      const updateChart = (date, type) => {
        let start = xScale.invert(handle1.attr('x1'))
        let end = xScale.invert(handle2.attr('x1'))
        // console.log('start', start)
        if (type === 'start') {
          start = date
        } else if (type === 'end') {
          end = date
        }

        // 确保 start 和 end 的顺序正确
        if (start > end) {
          [start, end] = [end, start]
        }
        handle1.attr('x1', xScale(start)).attr('x2', xScale(start))
        handle2.attr('x1', xScale(end)).attr('x2', xScale(end))
        triangleUp.attr('transform', `translate(${xScale(end)}, ${triUpOffsetY})`)
        triangleDown.attr('transform', `translate(${xScale(start)}, ${triDownOffsetY})`)
        label1
          .attr('x', xScale(start) - 50)
          .text(d3.timeFormat('%Y-%m-%d %H:%M')(start))
        label2.attr('x', xScale(end) - 40).text(d3.timeFormat('%Y-%m-%d %H:%M')(end))

        this.selTime1 =  (new Date(start)).getTime() * 1000
        this.selTime2 = (new Date(end)).getTime() * 1000
        // console.log('time', this.selTime1, this.selTime2)
        // console.log('time', d3.timeFormat('%Y-%m-%d %H:%M')(start), d3.timeFormat('%Y-%m-%d %H:%M')(end))
        // 更新遮罩
        mask.attr('x', xScale(start)).attr('width', xScale(end) - xScale(start))
      }

      // 创建遮罩定义
      const defs = svg.append('defs')
      // maskInRange
      defs
        .append('mask')
        .attr('id', 'mask-in-range')
        .append('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', chartWidth)
        .attr('height', chartHeight)
        .attr('fill', 'white')
      // maskOutOfRange
      defs
        .append('mask')
        .attr('id', 'mask-out-of-range')
        .append('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', chartWidth)
        .attr('height', chartHeight)
        .attr('fill', 'black')

      // 初始化柱子的遮罩效果
      svg
        .selectAll('.bar, .bar-complement')
        .data(data)
        .attr(
          'mask',
          (d) =>
            `url(#mask-${
              d.time >= xScale.invert(handle1.attr('x1')) &&
              d.time <= xScale.invert(handle2.attr('x1'))
                ? 'in-range'
                : 'out-of-range'
            })`
        )
    },
    commitTimeData(){
      this.$emit('sendData', {start_time: this.selTime1, end_time: this.selTime2})
      this.toggleTimeRange({
        start_time: this.selTime1,
        end_time: this.selTime2
      })
    }
  }//methods
}
</script>

<style>
*{
  margin: 0;
  padding: 0;
}
#timeline-chart{
  height: 70px;
  width: 700px;
  background-color: transparent;
  border-radius: 5px;
  z-index: 100;
  position: relative;
}
</style>