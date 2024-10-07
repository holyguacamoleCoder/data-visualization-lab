<template>
  <div class="app-container">
  <div class="header">
    <div class="title">
      XD-stClusterVis
    </div>
    <div class="filter">
      <span>Class:</span>
      <van-dropdown-menu>
        <van-dropdown-item v-model="selectedClasses" :options="classes" />
      </van-dropdown-menu>
    </div>
      

  </div>
  <div class="body">
    <div class="main">
      <div class="top">
        <!-- A. Scatter View -->
        <div class="scatter-view">
          <ScatterView />
        </div>
        
        <!-- B. Portrait View -->
        <div class="portrait-view">
          <PortraitView />
        </div>
      </div>
      
      <div class="bottom">
        <!-- C. Question View -->
        <div class="question-view">
          <QuestionView />
        </div>
        
        <!-- D. Question Tooltip -->
        <div class="week-view">
          <WeekView />
        </div>
      </div>
    </div>

    <!-- E. Student View -->
    <div class="panel">
       <div class="student-view">
         <StudentView />
       </div>
    </div>

    </div> 
  </div>

</template>

<script>
import ScatterView from './components/ScatterView.vue'
import PortraitView from './components/PortraitView.vue'
import QuestionView from './components/QuestionView.vue'
import WeekView from './components/WeekView.vue'
import StudentView from './components/StudentView.vue'
export default {
  components: {
    ScatterView,
    PortraitView,
    QuestionView,
    WeekView,
    StudentView
  },
  data() {
    return {
      selectedClasses: 2,
      classes:[
        {value: 1, text: 'Class 1'},
        {value: 2, text: 'Class 2'},
        {value: 3, text: 'Class 3'},
        {value: 4, text: 'Class 4'},
        {value: 5, text: 'Class 5'},
        {value: 6, text: 'Class 6'},
        {value: 7, text: 'Class 7'},
        {value: 8, text: 'Class 8'},
        {value: 9, text: 'Class 9'},
        {value: 10, text: 'Class 10'},
        {value: 11, text: 'Class 11'},
        {value: 12, text: 'Class 12'},
        {value: 13, text: 'Class 13'},
        {value: 14, text: 'Class 14'},
        {value: 15, text: 'Class 15'},
      ]
    }
  }
};
</script>

<style scoped lang="less">
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.app-container {

.header{
  width: 2100px;
  height: 50px;
  background-color: #2a2a2a;
  .title{
    float: left;
    color: #fff;
    font-size: 20px;
    font-weight: 700;
    margin-left: 20px;
    line-height: 50px;
  }
  .filter{
    float: right;
    margin-right: 20px;
    margin-top: 10px;
    width: 200px;
    height: 30px;
    border-radius: 5px;
    border: none;
    outline: none;
    color: #000;
    background-color: #fff;
    background-color: #fff;
    font-size: 16px;
  }
}
.body {
  width: 2100px;
  height: 1230px;
  display: flex;
  .main{
    width: 1700px;
    height: inherit;
    background-color: blue;
    display: flex;
    flex-direction: column;
    .top{
      width: inherit;
      height: 600px;
      display: flex;
      .scatter-view{
        width: 500px;
        height: inherit;
        background-color: yellow;
      }
      .portrait-view{
        width: 1400px;
        height: inherit;
        background-color: green;
      }
    }
    .bottom{
      width: inherit;
      height: 600px;
      display: flex;
      .question-view{
        width: 800px;
        height: inherit;
      }
      .week-view{
        width: 1200px;
        height: inherit;
        background-color: orange;
      }
    }
  }
  .panel{
    width: 400px;
    height: inherit;
    background-color: red;
  }
}

} //app-container
</style>
