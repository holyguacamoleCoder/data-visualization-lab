<template>
  <div class="right">
    <div class="distanceAnalyze">
      <div class="title">车辆车距变化</div>
      <div class="bar-chart"></div>
    </div>
    <div class="changeAnalyze">
      <div class="title">车辆变道情况</div>
      <div class="circular-chart">
      <div class="radar-chart">
        <div id="vizChord"></div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'RightComponent',
  data(){
    return{
      chordsData: []
    }
  },
  created(){
    // this.chordsData = {
    //   "id": 175202352,
    //   "data":{
    //     "nodes": [
    //         {"name": "66"},
    //         {"name": "1666"},
    //         {"name": "1686"},
    //         {"name": "1975"},
    //         {"name": "2311"},
    //         {"name": "2326"}
    //     ],
    //     "matrix": [
    //         [0, 0, 0, 1, 0, 0],  // Lane 66
    //         [0, 0, 0, 0, 0, 0],  // Lane 1666
    //         [0, 0, 0, 1, 0, 0],  // Lane 1686
    //         [1, 0, 0, 0, 0, 0],  // Lane 1975
    //         [0, 0, 0, 0, 0, 1],  // Lane 2311
    //         [0, 0, 0, 0, 0, 0]   // Lane 2326
    //     ]
    // }//data
          
    // }
  },
  mounted(){
  },
  computed: {
    ...mapState(['processData', 'hasGotData']),
  },
  methods: {
    renderChord(){
      const d3 = this.$d3
      const width = 120
      const height = 120
      const radius = Math.min(width, height) / 2 - 10
      const rowNum = 3
      const colNum = 3
      // create the svg area
      var svg = d3.select("#vizChord")
      .append("svg")
      .attr("width", (width + 4) * rowNum)
      .attr("height", (height + 4) * colNum)
      console.log('chordsData',this.chordsData)
      this.chordsData.forEach((item, index) => {
        // const id = item
        const data = item.data
        const ig = svg.append("g")
        .attr("transform", () => {
          const x0 = width / 2 + 2
          const y0 = height / 2 + 2
          const x = index % rowNum * (width + 4) + x0
          const y = Math.floor(index / colNum) * (height + 4) + y0
          return `translate(${x},${y})`
        })
        function sumMatrix(matrix){
          const flatMatrix = matrix.flat()
          return flatMatrix.reduce((a, b) => a + b, 0)
        }
        if (data.matrix.length === 1 && data.matrix[0].length === 1) {
          ig.append("g")
            .append("path")
            .style("fill", '#A0ACE6')
            .attr("d", d3.arc()
            .innerRadius(radius - 2)
            .outerRadius(radius)
            .startAngle(0)
            .endAngle(2 * Math.PI)
          )
          // 显示消息
          ig.append("text")
            .attr('transform', 'translate(0, -5)')
            .attr("text-anchor", "middle")
            .text("No lane changes detected.")
            .style("font-size", "9px")
          ig.append("text")
          .attr('transform', 'translate(0, 5)')
            .attr("text-anchor", "middle")
            .text(`Just for Lane ${data.nodes[0].name}`)
            .style("font-size", "9px")
        }
        else if(sumMatrix(data.matrix) == 0){
          ig.append("g")
            .append("path")
            .style("fill", '#CEE8E0')
            .attr("d", d3.arc()
            .innerRadius(radius - 2)
            .outerRadius(radius)
            .startAngle(0)
            .endAngle(2 * Math.PI)
          )
          // 显示消息
          ig.append("text")
            .attr('transform', 'translate(0, -5)')
            .attr("text-anchor", "middle")
            .text("Lane changed in crosswalk.")
            .style("font-size", "9px")
          ig.append("text")
          .attr('transform', 'translate(0, 5)')
            .attr("text-anchor", "middle")
            .text(`It is meaningless`)
            .style("font-size", "9px")
        }
        else{

          // console.log('data', data)
          const color = d3.scaleOrdinal(d3.schemeSpectral[11])
          // give this matrix to d3.chord(): it will calculates all the info we need to draw arc and ribbon
          var res = d3.chord()
          .padAngle(0.05)     // padding between entities (black arc)
          .sortSubgroups(d3.descending)(data.matrix)
          
          // Add the links between groups
          ig
          .datum(res)
          .append("g")
          .selectAll("path")
          .data(function(d) { return d; })
          .enter()
          .append("path")
          .attr("d", d3.ribbon()
              .radius(radius)
            )
            .style("fill", "#F8AC34")
            .style('opacity', (d, i) => (i + 1) * 0.2)
            
            // add the groups on the inner part of the circle
            const outerG = ig
            .datum(res)
            .append("g")
            .selectAll("g")
            .data(function(d) { return d.groups; })
            .enter()
            
            outerG.append("g")
            .append("path")
            .style("fill", (d, i) =>color(i))
            .attr("d", d3.arc()
            .innerRadius(radius - 2)
            .outerRadius(radius)
            )
          // console.log('d', this.chordsData.data.nodes[2].name)
          
          outerG.append("text")
          .each(function(d) { d.angle = (d.startAngle + d.endAngle) / 2; })
          .attr("dy", ".35em")
          .attr("transform", function(d) {
            return `rotate( ${d.angle * 180 / Math.PI - 90} )`
            + `translate(  ${(radius)} )`
            + (d.angle > Math.PI ? "rotate(180)" : "")
          })
          .style("text-anchor", function(d) { return d.angle > Math.PI ? "end" : null; })
          .text((d, i) => data.nodes[i].name)
          .style("font-size", "5px")
        }//else
              
    
      })// forEach
          
    }// renderChord  
  }, //methods
  watch:{
    hasGotData: {
      handler() {
        this.chordsData = []
        Object.entries(this.processData).forEach(item=>{
          this.chordsData.push({
            id:item[0],
            data:item[1].change_lane,
          })
          // console.log('change_lane' )
        })
        // console.log(this.chordsData)
        this.$d3.select('#vizChord').selectAll('*').remove()
        this.renderChord()
      },
      deep: true
    }
  }//watch
};
</script>

<style lang="less">
.right {
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-radius: 5px;
  height: 460px;
}
.changeAnalyze, .distanceAnalyze{
  .title{
    position: relative;
    border-radius: 5px 5px 0 0;
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
}
.bar-chart{
  border-radius: 0 0 5px;
  background-color: #fff;
  height: 165px;
}
.circular-chart {
  border-radius: 0 0 5px;
  background-color: #fff;
  height: 250px;
}
</style>
