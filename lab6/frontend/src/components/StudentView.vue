<template>
  <div class="scrollBarWrap" id="student-view" data-simplebar>
    <div class="title">Student View</div>
    <Simplebar style="height: 1170px">
      <div ref="studentContainer" class="student" v-for="item, index in treeData['children']" :key="index" >
        <p>{{item['name']}}</p>
        <div ref="studentChart" class="chart" ></div>
      </div>
    </Simplebar>
  </div>
</template>

<script>
import axios from 'axios'
import Simplebar from 'simplebar-vue'
import 'simplebar-vue/dist/simplebar.min.css'
export default {
  name: 'StudentView',
  components: {
    Simplebar
  },
  data() {
    return {
      submissions: [],
      treeData: [],
    }
  },
  async created(){
  },
  async mounted() {
    // this.fetchTreeData()
    // this.renderTree()
    // this.renderEveryStudents()
  },
  updated() {
    console.log(this.$refs.studentContainer)
  },
  methods: {
    async fetchTreeData() {
      try {
        const response = await axios.get('http://localhost:5000/api/tree_data', {
          params: {
            limit: 10,
          }
        });
        this.treeData = response.data;
        // console.log('TreeData:', this.treeData);
        this.renderEveryStudents()
      } catch (error) {
        console.error('Failed to fetch treeData:', error);
      }
    },

    renderTree(tree_data){
      // console.log('renderTree')
      if(!tree_data || tree_data['children'].length === 0) return
      // 创建svg画布
      this.$nextTick(() =>{

      // console.log(this.$refs.studentContainer)
      this.$refs.studentContainer.forEach((chart) => {
        const svgChart = chart.childNodes[1]
        // console.log(svgChart)
        // 渲染函数
        const lineLength = 100
        const svg = this.$d3.select(svgChart).append('svg')
        .attr('width', 390)
        .attr('height', 70 )
        const g = svg.append('g').attr('transform', 'translate(80, 0)')
        const radius = 5
        // 渲染函数
        const render = (tree) => {
        g.selectAll('path').data(tree.links()).join('path')
        .attr('fill', 'none')
        .attr('stroke', 'black')
        .attr('d', this.$d3.linkHorizontal().x(d => d.y).y(d => d.x))
        // 树的连接线
        g.selectAll('line').data(tree.descendants()).join('line')
        .attr('x1', 0)
        .attr('x2', 50)
        .attr('y1', 20)
        .attr('y2', 20)
        .attr('fill', '#000')
         // 此次提交分数
         g.selectAll('.base-line').data(tree.descendants()).join('rect')
        .attr('class', 'base-line')
        .attr('x', d => d.y)
        .attr('y', d => d.x - radius / 2 + 1)
        .attr('width', d => d.children ? 0 : lineLength)
        .attr('height', 3)
        .attr('fill', '#237CAF')
        .attr('rx', 2)
        .attr('ry', 2)
        // 节点
        g.selectAll('circle').data(tree.descendants()).join('circle')
        .attr('cx', d => d.y + d.data.times * 10)
        .attr('cy', d => d.x)
        .attr('r', radius)
        .attr('fill', 'red')
        .attr('stroke', 'black')
        // 题目提交状态
        g.selectAll('text').data(tree.descendants()).join('text')
        .attr('x', d => d.y + (d.children ? -radius - 1 : radius + 5))
        .attr('y', d => d.x + radius / 2 - radius * 3 / 2)
        .text(d => d.data.name)
        .attr('font-size', '10px')
        .attr('text-anchor', d => d.children ? 'end' : 'start') 
        // 此次提交分数
        g.selectAll('.score-line').data(tree.descendants()).join('rect')
        .attr('class', 'score-line')
        .attr('x', d => d.y + radius + lineLength)
        .attr('y', d => d.x - radius / 2)
        .attr('width', d => (d.data.value ? d.data.value : 0) * 10) // 假设 values 是数值类型
        .attr('height', 5)
        .attr('fill', '#237CAF')
        .attr('rx', 2)
        .attr('ry', 2)
      }
      
      
      // 处理json数据，计算树的高度
      const root = this.$d3.hierarchy(tree_data)
      // 定义一个树形布局,并映射为具体位置
      const tree = this.$d3.tree()
                  .size([70, 70])(root)
      // console.log(tree)
      // 渲染
      render(tree)

    })// 循环每个学生
  })//nextTick

    },

    renderEveryStudents(){
      console.log('renderEveryStudents')
      var student = this.treeData.children[0]
      console.log(student)

      var renderQuestions = (student) => {
        student.children.forEach((elem) => {
          var question = elem
          // console.log(question)
          question.name = question.name.slice(-5)
          this.renderTree(question)
        })
      }

      renderQuestions(student)
    }
  }// methods
};
</script>

<style scoped lang="less">
#student-view {
  width: 400px;
  height: 1200px;
 
  .title{
    font-size: 20px;
    font-weight: bold;
    margin-left: 10px;
    margin-top: 10px;
    padding: 5px;
    padding-top: 0;
    border-bottom: 1px solid #ccc;
  }
 
    .student{
      width: 345px;
      height: auto;
      margin-left: 20px;
      margin-top: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
      background-color: #fff;
      p{
        margin-left: 10px; 
      }
    }
}
/deep/ .simplebar-vertical {
  width: 16px;
}
</style>
