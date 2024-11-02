<template>
  <div class="middle">
    <div class="toggleBox">
      <button class="toggleButton flushButton" @click="handleFlushClick">
        <span class="iconfont icon-shuaxin"></span>
      </button>
      <button class="toggleButton pauseButton" @click="handlePauseClick">
        <span class="iconfont icon-jixu" v-if="!isPlaying"></span>
        <span class="iconfont icon-zanting1" v-if="isPlaying"></span>
      </button>
      <button class="toggleButton" @click="handleBrushButton">
        <span class="iconfont icon-appsSelect"></span>
      </button>
      <button class="toggleButton" 
        :style="{opacity: selectedList.length ? '1' : '0.5'}"
        @click="handleAnalyzeButton">
        <span class="iconfont icon-loading" v-if="isLoading"></span>
        <span class="iconfont icon-weibiaoti1" v-if="!isLoading"></span>
      </button>
    </div>
    <div class="traffic-map">
      <div class="legend">
        <div class="vehicleLegend">
          <div class="pedestrian" v-for="(item, index) in 
            renderVehicle" 
            :key="index">
            <span class="label" :style="{ backgroundColor: item[1] }"></span>
            <span>{{item[2]}}</span>
          </div>
        </div>
        <div class="roadLegend">
          <div class="virRoad">
            <span class="label"></span>
            <span>虚拟车道</span>
          </div>
          <div class="crossWalk">
            <span class="label"></span>
            <span>人行横道</span>
          </div>
          <div class="stopLine">
            <span class="label"></span>
            <span>停车线</span>
          </div>
          <div class="roadLine">
            <span class="label"></span>
            <span>车道线</span>
          </div>
          <div class="signal">
            <span class="label"></span>
            <span>红绿灯</span>
          </div>
        </div>
      </div>
      <div class="detail">
        <div>ID：202808709</div>
        <div>速度：5.248671</div>
        <div>帧数：280658642</div>
        <div>类型：小型车辆</div>
        <div>车头朝向：-27.49 degrees</div>
      </div>
      <v3-drag-zoom-container
        style="width: 700px; height: 460px; background-color: #fff;"
        align="cover"
        reset
      >
        <div id="map-chart" style="transform: scale(3) scaleY(-1)"></div>
      </v3-drag-zoom-container>
      <button class="filterTimeButton" @click="fetchTimelineData">
        <span class="iconfont icon-shaixuan"></span>
      </button>
    </div>
    <TimelineSlider 
      ref="timeline"
      @sendData="handleTimelineData"  
    />
  </div>
</template>

<script>
import { getMapData, getTrafficData } from '@/api/MiddleComponent'
import { mapActions } from 'vuex'
import TimelineSlider from '@/components/TimelineSlider.vue'
import { V3DragZoomContainer } from "v3-drag-zoom"
import "v3-drag-zoom/dist/style.css"
export default {
  name: 'MiddleComponent',
  data() {
    return {
      chart: null,
      geoJsonRoadData: null,
      trafficData: null,
      start_time: 0,
      end_time: 0,
      svg: null,
      g: null,
      rects: null,
      frame: 16.67,
      isPlaying: true,
      intervalId: null,
      isBrushing: false,
      isLoading: false,
      allVehicles: {},
      selectedList: [],
      enumVehicle: [
        ['UNKNOWN', 'red'], //未识别
        ['CAR', '#FECB5C'], //小型车辆
        ['PEDESTRIAN', '#EA6175'], //行人
        ['CYCLIST', '#85E4FF'], //非机动车
        ['TRUCK', '#217EB7'], //卡车
        ['VAN', '#C9C981'], //厢式货车、面包车
        ['BUS', '#FF9374'], //客车
        ['STATIC', '#CDCDCD'], //静态物体
        ['STATIC_EDGE', 'yellow'], //路牙
        ['CONE', '#FFFF1F'], //锥桶
        ['TROLLEY', '#BBC8FF'], //手推车、三轮车
        ['ROBOT', '#12BB7D'], //信号灯
        ['GATE', 'green'] //门、阀门、闸机、出入口
      ],
      renderVehicle: [
        ['CAR', '#FECB5C', '小型车辆'], //小型车辆
        ['PEDESTRIAN', '#EA6175', '行人'], //行人
        ['CYCLIST', '#85E4FF', '非机动车'], //非机动车
        ['TRUCK', '#217EB7', '卡车'], //卡车
        ['BUS', '#FF9374', '客车'], //客车
        ['TROLLEY', '#BBC8FF', '手推/三轮车'], //手推车、三轮车
      ],
    }
  },
  components: {
    TimelineSlider,
    V3DragZoomContainer,
  },
  async mounted() {
    const controlMap = async () => {
      const { data } = await getMapData()
      this.geoJsonRoadData = data
      // console.log(this.geoJsonRoadData)
      this.renderRoad()
    }
    controlMap()
  },
  computed: {
  },
  methods:{
    ...mapActions(['fetchProcessData', 'toggleHasGotData']),
    transformItem(coordinate){
        return [coordinate[0], -1 * coordinate[1], coordinate[2]]
    },
    renderRoad(){
      const d3 = this.$d3
      // 设置 SVG 容器
      const width = 700
      const height = 600
      const data = this.geoJsonRoadData
      const svg = d3.select("#map-chart")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
      this.svg = svg
      // 设置路径生成器
      const path = d3.geoPath()
      const g = svg.append("g")
      .attr("transform", `translate(${380}, ${420})`)
      this.g = g
      // 绘制多边形
      const polygons = data.filter(feature => feature.geometry.type === "Polygon")
      // const polygonsData = this.transformData(polygons)
      // console.log('p',polygons)
      polygons.forEach(polygon => {
        const transformPoly = polygon
        // {
        //   ...polygon,
        //   geometry: {
        //     ...polygon.geometry,
        //     coordinates: [polygon.geometry.coordinates[0].map(item => this.transformItem(item))]
        //   }
        // }
        // console.log('tp', polygon.geometry.coordinates[0].map(item => this.transformItem(item)))
        g.append("path")
          .datum(transformPoly)
          .attr("d", path)
          .attr("fill", "#ccc")
        })

      // 绘制线段
      const lines = data.filter(feature => feature.geometry.type === "LineString")
      // console.log('l',lines)
      lines.forEach(line => {
        const transformLine = line
        // {
        //   ...line,
        //   geometry: {
        //     ...line.geometry,
        //     coordinates: line.geometry.coordinates.map(item => this.transformItem(item))
        //   }
        // }
        g.append("path")
          .datum(transformLine)
          .attr("d", path)
          .attr("stroke", d => {
            if(d.properties.vir === 1) return "#000" // virtual road
            else if (d.properties.lane_no) return "#A0ACE6" //road
            else if(d.geometry.coordinates.length === 2) return "red" //stop line
            if(d.properties.turn_type === 0) return "#C4F6E5" // 非转弯车道
            else if(d.properties.turn_type){
              if(d.properties.turn_type === 1) return "#A0ACE6" // 直行车道
              else if(d.properties.turn_type === 2) return "#CBEDB1" // 左转车道
              else if(d.properties.turn_type === 3) return "#C3F6E5" //  右转车道
              else if(d.properties.turn_type === 4) return "#AEC6F1" //  掉转车道
            }
            else return "#000" // straight line
          })
          .attr("stroke-width", 0.3)
          .attr('opacity', 0.7)
          .attr("fill", "none")
          .style('stroke-dasharray', d => d.properties.vir === 1 ? '4, 3' : '0')
      })

      // 绘制点
      const points = data.filter(feature => feature.geometry.type === "Point")
      // console.log('points',points)
      points.forEach(point => {
        const transformPoint = point
        // {
        //   ...point,
        //   geometry: {
        //     ...point.geometry,
        //     coordinates: this.transformItem(point.geometry.coordinates)
        //   }
        // }
        g.append("circle")
          .attr("cx", path.centroid(transformPoint)[0])
          .attr("cy", path.centroid(transformPoint)[1])
          .attr("r", 1)
          .attr("fill", "green")
      })
    },
    renderTraffic(){
      const d3 = this.$d3
      // const data = this.trafficData
      // console.log('data', data)
      this.rects = this.g.selectAll('.vehicleCircle')
      .data(Object.values(this.allVehicles)) // 使用 id 作为键值，确保唯一性
      .join(
        enter => enter.append('rect')
        .attr('class', 'vehicleCircle')
        .attr('x', d => JSON.parse(d.position).x)
        .attr('y', d => JSON.parse(d.position).y)
        .attr('width',  d => JSON.parse(d.shape).x)
        .attr('height', d => JSON.parse(d.shape).y)
        .attr('rx',  d => JSON.parse(d.shape).x/8)
        .attr('transform', d => {
          const angle = d.orientation * 180 / Math.PI
          const cx = parseFloat(JSON.parse(d.position).x) + parseFloat(JSON.parse(d.shape).x / 2)
          const cy = parseFloat(JSON.parse(d.position).y) + parseFloat(JSON.parse(d.shape).y / 2)
          return `rotate(${angle}, ${cx}, ${cy})`
        }) 
        .attr('fill', d => d.type >= 0 ? this.enumVehicle[d.type][1] : 'none')
        .attr('opacity', 0.7)
        .attr('stroke', 'black')
        .attr('stroke-width', 0.2)
        .on('mouseover', (e, d) =>{
          d3.select('.detail').html(() => {
            console.log('d', d)
            return  `<div>ID：${d.id}</div>
            <div>速度：${d.velocity} m/s</div>
            <div>帧数：${d.seq}</div>
            <div>类型：${d.type}</div>
            <div>车头朝向：${d.orientation}</div>`
          })
        })
        .on('mouseout', function(){
          d3.select('detail').html('')
        })
        .on('click', (e, d) => {
          this.handleSelect(e, d)
        }),
      
        update => update
        .transition()
        .duration(this.frame)
        .ease(this.$d3.easeQuadInOut)
        .attr('x', d => JSON.parse(d.position).x)
        .attr('y', d => JSON.parse(d.position).y)
        .attr('transform', d => {
          const angle = d.orientation * 180 / Math.PI
          const cx = parseFloat(JSON.parse(d.position).x) + parseFloat(JSON.parse(d.shape).x / 2)
          const cy = parseFloat(JSON.parse(d.position).y) + parseFloat(JSON.parse(d.shape).y / 2)
          return `rotate(${angle}, ${cx}, ${cy})`
        }) 
        .attr('fill', d => d.type >= 0 ? this.enumVehicle[d.type][1] : 'none'),
        
        exit => exit.transition()
        .duration(this.frame) // 500毫秒的退出动画
        .ease(this.$d3.easeQuadInOut)
        .attr('opacity', 0)
        .remove()
      )
    },
    renderInTime(){
      if(this.trafficData === null){return}
      // 初始化索引用于遍历时间戳
      let currentIndex = 0
      const allData = this.trafficData
      // 定义一个函数来更新数据并调用 renderTraffic
      const updateTraffic = () => {
        // 检查是否还有更多的数据
        if (currentIndex < allData.length) {
         // 获取当前时间戳的数据
        const currentData = allData[currentIndex].items
        // 调用你的 renderTraffic 函数
        this.renderTraffic(currentData)
        updateVehiclesState(currentData)
    
        // 更新索引
        currentIndex++
        
        // this.frame = (allData[currentIndex].time_meas - allData[currentIndex - 1].time_meas) / 1000
        // console.log('frame', frame)
        // 设置下一帧的时间，这里假设每秒更新一次数据
        this.intervalId = setTimeout(updateTraffic, this.frame) // 使用 setTimeout 模拟动画帧
        } else {
          // 如果没有更多数据，可以停止或者重置
          console.log("所有时间戳的数据已渲染完毕");
          // 重置索引以便再次播放
         currentIndex = 0;
          // 可以选择再次开始
          // updateTraffic();
        }
      }
      // 更新全局车辆状态
      const updateVehiclesState = (currentData) => {
        // 添加或更新当前时间戳的数据
        currentData.forEach(item => {
          this.allVehicles[item.id] = item;
        })
      
        // // 移除不再存在于当前时间戳的数据
        // const currentIds = new Set(currentData.map(item => item.id));
        // Object.keys(this.allVehicles).forEach(id => {
        //   if (!currentIds.has(id)) {
        //     delete this.allVehicles[id];
        //   }
        // })
      }
      // 开始渲染第一个时间戳的数据
      updateTraffic()
    },
    renderBrush(){
      const d3 = this.$d3
      const width = this.svg.attr('width')
      const height = this.svg.attr('height')
      // Add brushing
      this.g
         .call( d3.brush()                 // Add the brush feature using the d3.brush function
           .extent( [ [0,0], [width,height] ] ) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
           .on("start brush", () => {
              console.log('extent', d3.event)
              const extent = d3.event.selection
              this.rects.classed("selected", function(d){ 
                console.log('d', d)
                return isBrushed(extent, JSON.parse(d.position).x, JSON.parse(d.position).y) } )
           }) // Each time the brush selection changes, trigger the 'updateChart' function
         )

       // Function that is triggered when brushing is performed
       // A function that return TRUE or FALSE according if a dot is in the selection or not
       function isBrushed(brush_coords, cx, cy) {
            var x0 = brush_coords[0][0],
                x1 = brush_coords[1][0],
                y0 = brush_coords[0][1],
                y1 = brush_coords[1][1];
           return x0 <= cx && cx <= x1 && y0 <= cy && cy <= y1;    // This return TRUE or FALSE depending on if the points is in the selected area
       }      
    },
    handleFlushClick(){
      // const d3 = this.$d3
      this.handlePauseClick()
      this.selectedList = []
      this.allVehicles = {}
      clearTimeout(this.intervalId)
      this.isPlaying = !this.isPlaying
      this.svg.selectAll('*').remove()
      this.renderRoad()
      this.renderInTime()
      this.handlePauseClick()
    },
    handlePauseClick(){
      this.isPlaying = !this.isPlaying
      if (this.isPlaying) {
        this.renderInTime()
      } else {
        clearTimeout(this.intervalId) // 暂停动画
      }
    },
    handleBrushButton(){
      this.handleClick()
      console.log('renderBrush!!')
      console.log('g',this.g)
      this.isBrushing = !this.isBrushing
      if (this.isBrushing) {
        this.renderBrush()
      } else {
        this.svg.selectAll('.selected').classed('selected', false)
      }
    },
    handleSelect(e, d){
      const elem = e.target
      // console.log(elem.classList.contains('selectedV'))
      if(elem.classList.contains('selectedV')){
        elem.style["stroke-width"] = 0.2
        elem.style["opacity"] = 0.7
        elem.classList.remove('selectedV')
        this.selectedList = this.selectedList.filter(item => item !== d.id)
      } else {
        elem.classList.add('selectedV')
        e.target.style["stroke-width"] = 0.7
        e.target.style["opacity"] = 1
        this.selectedList.push(d.id)
      }
      console.log('selectedList', this.selectedList)
      // console.log('click', d.id)
    },
    async handleAnalyzeButton(){
      this.isLoading = true
      //将选择列表提交给后端进行分析
      // const params = {
      //   start_time: 1681316252099657,
      //   end_time: 1681316700099673,
      //   ids: this.selectedList
      // }
      const params = {
        start_time: this.start_time,
        end_time: this.end_time,
        ids: this.selectedList
      }
      await this.fetchProcessData(params)
      this.$d3.select('#acceleration-chart').selectAll('*').remove()
      this.$d3.select('#speed-chart').selectAll('*').remove()
      this.$d3.select('#line-chart').selectAll('*').remove()
      this.toggleHasGotData()
      this.isLoading = false
    },
    fetchTimelineData(){
      // console.log('refs:',this.$refs.timeline)
      this.$refs.timeline.commitTimeData()
    },
    handleTimelineData(timelineData){
      console.log('timelineData',timelineData)
      const {start_time, end_time} = timelineData
      this.start_time = start_time
      this.end_time = end_time
      const controlTraffic = async () => { 
      const params = {
        start_time,
        end_time,
        group: true
      }
      // const params = {
      //   start_time: 1681316252099657,
      //   end_time: 1681316700099673,
      //   group: true
      // }
      const { data } = await getTrafficData(params)
      this.trafficData = data
      // console.log('trafficData', this.trafficData)
      this.renderInTime()
      this.handlePauseClick()
    }

    controlTraffic()
      // const params = data
    }
  }//methods
}
</script>

<style lang="less">
.selected {
  opacity: 1 !important;
  stroke: black;
  stroke-width: 1px;
}

.middle {
  position: relative;
  border-radius: 5px;
  width: 700px;
  height: 460px;
  .toggleBox{
    position: absolute;
    top: 0px;
    left: 0px;
    z-index: 15;
    margin-top: 10px;
    margin-left: 10px;
    width: 145px;
    display: flex;
    justify-content: space-between;
    .toggleButton{
      height: 30px;
      width: 30px;
      border-radius: 25px;
      background-color: #A0ACE6;
      color: #fff;
      border: 0;
      
    }
  }
}
.filterTimeButton{
  position: absolute;
  display: block;
  top: 370px;
  left: 0px;
  height: 30px;
  width: 80px;
  border-radius: 0 20px  20px 0;
  background-color: #A0ACE6;
  color: #fff;
  border: 0;
  z-index: 100;
}
.traffic-map {
  height: 400px;
  width: 700px;
  position: relative;
  .legend{
    display: flex;
    position:absolute;
    height: 100px;
    width: 170px;
    top: 0;
    right: 0px;
    z-index: 2;
    font-size: 9px;
    font-weight: 900;
    .vehicleLegend{
      z-index: 5;
      display: flex;
      flex: 2;
      flex-direction: column;
      justify-content: space-around;
      align-items: center;
      margin-left: 12px;
      .pedestrian{
        .label{
          display: inline-block;
          width: 7px;
          height: 7px;
          margin-right: 6px;
          border-radius: 2px;
          background-color: #ccc;
        }
      }
    }
    .roadLegend{
      margin-right: 2px;
      z-index: 5;
      display: flex;
      flex: 3;
      flex-direction: column;
      justify-content:space-around;
      align-items: center;
      .virRoad{
        .label{
          display: inline-block;
          width: 35px;
          height: 7px;
          margin-right: 3px;
          border-top: 1px dashed #333;
          border-bottom: 1px dashed #000;
        }
      }
      .crossWalk{
        .label{
          display: inline-block;
          width: 35px;
          height: 7px;
          margin-right: 3px;
          background-color: #ccc;
        }
      }
      .stopLine{
        .label{
          display: inline-block;
          width: 35px;
          height: 3px;
          margin-right: 3px;
          border-top: 1px solid red;
        }
      }
      .roadLine{
        .label{
          display: inline-block;
          width: 35px;
          height: 5px;
          margin-right: 3px;
          border-top: 1px solid #C4F7E4;
          border-bottom: 1px solid #A0ACE6;
        }
      }
      .signal{
        .label{
          display: inline-block;
          width: 7px;
          height: 7px;
          margin-right: 3px;
          border-radius: 5px;
          background-color: green;
        }
      }
    }
  }
  .legend::before{
    content: '';
    display: block;
    position: absolute;
    width: 170px;
    height: 100px;
    border: 1px solid #A0ACE6;
    background-color: #fff;
    opacity: 0.5;
    border-radius: 0 5px 0 0;
  }
  .detail{
    position: absolute;
    z-index: 5;
    top: 40%;
    right: 0;
    height: 100px;
    width: 150px;
    background-color: transparent;
    font-size: 10px;
    font-weight: 550;
  }
}
</style>
