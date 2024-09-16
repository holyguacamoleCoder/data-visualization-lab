<template>
  <div class="app-container">
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
  width: 2100px;
  height: 1200px;
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
        width: 700px;
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


</style>
