import { createApp } from 'vue';
import App from './App.vue';
import * as echarts from 'echarts';
import * as d3 from 'd3';

const app = createApp(App);
app.config.globalProperties.$echarts = echarts;
app.config.globalProperties.$d3 = d3;
app.mount('#app');
