<template>
  <div class="dashboard-container">
    <!-- 1. 标题部分 -->
    <!-- 1. 标题部分 -->
    <div class="title">
      车辆驾驶画像可视化分析
    </div>

    <!-- 2. 主内容部分 -->
    <div class="main">
      <LeftComponent />
      <MiddleComponent />
      <RightComponent />
    </div>

    <!-- 3. 底部部分 -->
    <BottomComponent />
    <!-- {{ processData }} -->
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import LeftComponent from './components/LeftComponent.vue'
import MiddleComponent from './components/MiddleComponent.vue'
import RightComponent from './components/RightComponent.vue'
import BottomComponent from './components/BottomComponent.vue'

export default {
  name: 'App',
  components: {
    LeftComponent,
    MiddleComponent,
    RightComponent,
    BottomComponent,
  },
  data() {
    return {
    }
  },
  computed: {
    ...mapState(['processData']),
  },
  created() {
  },
  // async mounted() {
  //   const params = {
  //     start_time: 1681316252099657,
  //     end_time: 1681316700099673,
  //     ids: [175202352, 172577571]
  //   }
  //   await this.fetchProcessData(params)
  //   this.toggleHasGotData()
  // },
  methods: {
    ...mapActions(['fetchProcessData', 'toggleHasGotData']),
  }
};
</script>

<style lang="less">
*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 10px;
  background-color: #E9ECF9;
  width: 1440px;
  height: 770px;
}
.title {
  height: 40px;
  width: 1420px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  background-color: #fff;
}

.main {
  display: grid;
  grid-template-columns: 300px 700px 400px;
  gap: 10px;
  height: 510px;
}
.bottom {
  display: grid;
  grid-template-columns: 500px 200px 700px;
  gap: 10px;
  height: 260px;
}
</style>
