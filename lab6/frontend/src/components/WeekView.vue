<template>
  <div id="week-view" style="height: 400px;">
    <h3>Week View</h3>
    <Simplebar style="height: 500px">
      <div id="visualizationW"></div>
    </Simplebar>
  </div>
</template>

<script>
import axios from 'axios'
import Simplebar from 'simplebar-vue'
import 'simplebar-vue/dist/simplebar.min.css'
export default {
  name: 'WeekView',
  data() {
    return {
      WeekData: []
    };
  },
  components: {
    Simplebar
  },
  async mounted() {
    // this.getWeekData()
  },
  methods: {
    async getWeekData() {
      // 获取题目数据
      try {
        const response = await axios.get('http://localhost:5000/api/week', {
          params: {
          }
        });
        this.WeekData = response.data;
        console.log('WeekData:', this.WeekData);
        this.renderWeekData()
      } catch (error) {
        console.error('Failed to fetch Week:', error);
      }
    },
    renderWeekData(){
      // console.log('renderWeekData')
      const d3 = this.$d3
      const data = this.WeekData
      const height = 600
      const width = 790
      const margin = {top: 20, bottom: 20, left: 20, right: 20} 
      const stu_icon = 40
    
      //定义维度
      const numWeeks = d3.max(data.students, d => d.weeks.length)
      const numStudents = data.students.length
      const stu_ids = Object.values(data.students).map(d => d.id.slice(-5))
      // const numKnowledgePoints = 8
      // console.log('numWeek', numWeeks)
      // console.log('numStudents', numStudents)
      // console.log('stu_id', stu_ids)
      
      const svg = d3.select('#visualizationW')
        .append('svg')
        .attr('width',width / 10 * numWeeks)
        .attr('height', (height / 5) * numStudents)
      const g = svg.append('g')
        .attr('transform', `translate(${margin.left + stu_icon}, ${margin.top})`)
      // console.log('g:',g)

      
      // 定义缩放尺
      const weekX = d3.scaleLinear()
      .domain([0, numWeeks])
      .range([0, width / 10 * numWeeks])
      // .padding(0.1)

      const studentsY = d3.scaleBand()
      .domain(stu_ids)
      .range([0, (height / 5) * numStudents])
      // .padding(0.1)
      // console.log('studentY', studentsY)

      // 定义坐标轴
      const xAxis = d3.axisTop(weekX)
      const yAxis = d3.axisLeft(studentsY)

      // 绘制坐标轴
      g.append('g').call(xAxis)
      g.append('g').call(yAxis)
      
      // 区分x轴,奇数填充为深色列
      const deepData = [1, 3, 5, 7, 9, 11, 13, 15]
      g.selectAll('.deepArea')
      .data(deepData)
      .enter()
      .append('g')
      .append('rect')
        .attr('x', d => weekX(d) - width / 20 )
        .attr('fill', '#F5F5F5')
        .attr('width', width / 10)
        .attr('height', (height / 5) * numStudents)


      // ------------------每个元素：Bar Radar部分-----------------
      const radius = 40
      const innerRadius = 0.4 * radius
      const outerRadius = radius
      const knowledge = Object.keys(data.students[0].weeks[0].scores)
      // console.log('knowledge', knowledge)
      // 定义角度缩放尺
      const angleX = d3.scaleBand()
        .domain(knowledge)
        .range([0, 2 * Math.PI])
        .align(0)
      // 定义半径缩放尺
      const radiusY = d3.scaleLinear()
      .domain([0, 1])
      .range([innerRadius, outerRadius])
      // 定义曲线生成器
      const arc = d3.arc()
          .innerRadius(innerRadius)
          .outerRadius(d => radiusY(d.value))
          .startAngle(d => angleX(d.knowledge))
          .endAngle(d => angleX(d.knowledge) + angleX.bandwidth())
          .padAngle(0.01)
          .padRadius(innerRadius)
      
      const radarData = Object.values(data)[0]
      // console.log('Ovdata:', radarData)
      const transform =  function(scores){
          return Object.entries(scores).map((d) => {
            return {
              'knowledge': d[0], 
              'value': d[1], 
            }
          })
        }
      radarData.length = 1
      // console.log(radarData)
      // 对每个学生
      radarData.forEach((s) => {
        // console.log('s:', s)
        const student_id = s.id
        const student_weeks = s.weeks
        
        // 对每一周
        student_weeks.forEach(w => {
          const position = `translate(${weekX(w.week) + width / 10}, ${studentsY(student_id.slice(-5)) + studentsY.bandwidth() / 2})`
          const radarChartG = g.append('g')
            .attr('class','radar')
            .attr("transform", position)
          //绘制柱状图
          radarChartG.selectAll('.radar')
          .data(transform(w.scores))
          .enter()
          .append('g')
          .append("path")
            .attr('fill', `${'#12e5bf'}`)
            .attr('d', arc)

          // console.log('w:', transform(w.scores))
          // console.log('w.week',w.week)
          // console.log('student_id', student_id)
      

          // 绘制标签圆
          const labelOuterRadius = innerRadius
          const labelInnerRadius = 0.7 * labelOuterRadius
          const innerCircleRadius = 0.8* labelInnerRadius
          const labelArc = d3.arc()
              .innerRadius(d => d.r1)
              .outerRadius(d => d.r2)
              .startAngle(0)
              .endAngle(Math.PI * 2)

          const circleOuterData = [{
            r1: labelInnerRadius,
            r2: labelOuterRadius
          }]
          const circleInnerData = [{
            r1: 0,
            r2: innerCircleRadius
          }]
          const labelOG = g.append('g')
            .attr('class','label-circle')
            .attr("transform", position)
          // console.log('labelG', labelG)
          const labelG = g.append('g')
            .attr('class','label-circle')
            .attr("transform", position)

          labelOG.selectAll('.label-circle')
          .data(circleOuterData)
          .enter()
          .append('g')
          .append("path")
            .attr('fill', `${'#FFFFFF'}`)
            .attr('d', labelArc)

          labelG.selectAll('.label-circle')
          .data(circleInnerData)
          .enter()
          .append('g')
          .append("path")
            .attr('fill', `${'#FFFFFF'}`)
            .attr('d', labelArc)


        })//forEach.w

      }) // forEach.s
      
    }
  }
};
</script>

<style scoped lang="less">
#week-view {
  width: 100%;
  h3{
    height: 20px;
    width: inherit;
    font-size: 20px;
    padding: 0 10px 10px;
    margin: 10px 5px;
    border-bottom: 1px solid #ccc;
  }
}
</style>
