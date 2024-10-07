import { createApp } from 'vue';
import App from './App.vue';
import * as echarts from 'echarts';
import * as d3 from 'd3';
import { DropdownMenu, DropdownItem } from 'vant';
// import Simplebar from 'simplebar-vue'
// import 'simplebar-vue/dist/simplebar.min.css'




const app = createApp(App);
app.config.globalProperties.$echarts = echarts;
app.config.globalProperties.$d3 = d3;
//滚动条组件
// app.use(simplebar)
// 下拉菜单组件注册
app.use(DropdownItem);
app.use(DropdownMenu);
app.mount('#app');
