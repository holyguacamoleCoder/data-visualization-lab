import { createStore } from 'vuex'
import { getProcessByIds } from '@/api/App'

export default createStore({
  state: {
    processData: null,
    hasGotData: false,
    timeRange: {
      start_time: 0,
      end_time: 0
    }
  },
  mutations: {
    setProcessData(state, data){
      state.processData = data
    },
    setHasGotData(state){
      state.hasGotData = !state.hasGotData
    },
    setTimeRange(state, data){
      const { start_time, end_time } = data 
      state.timeRange = {
        start_time,
        end_time
      }
    }
  },
  actions: {
    async fetchProcessData(context, params) {
      const { data } = await getProcessByIds(params)
      console.log('data', data)
      context.commit('setProcessData', data)
      console.log('processData', this.state.processData)
    },
    toggleHasGotData(context){
      console.log('toggleHasGotData')
      context.commit('setHasGotData')
    },
    toggleTimeRange(context, data){
      context.commit('setTimeRange', data)
    }
    // toggleSelection(context, student_id){
    //   context.commit('setSelectedStudents', student_id)
    //   context.commit('setStudentData')
    //   console.log('selectStudentData', this.state.selectedStudentData)
    // },
  },
  getters: {
    // getProcessData(state){
    //   return state.processData
    // }
  }
})