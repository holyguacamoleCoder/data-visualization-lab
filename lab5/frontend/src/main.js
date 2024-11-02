import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import * as echarts from 'echarts'
import * as d3 from 'd3'
import '@/assets/icon/iconfont.css'
// import V3DragZoom  from 'v3-drag-zoom'

// import Simplebar from 'simplebar-vue'
// import 'simplebar-vue/dist/simplebar.min.css'


const app = createApp(App)
app.use(store)
app.config.globalProperties.$echarts = echarts
app.config.globalProperties.$d3 = d3
// app.use(V3DragZoom)
app.mount('#app')
//滚动条组件
// app.use(simplebar)
