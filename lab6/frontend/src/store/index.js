import { createStore } from 'vuex'
import { getClusters } from '@/api/WeekView'


export default createStore({
  state: {
    clusterData: null,
    justClusterData: null
  },
  mutations: {
    setClusterData(state, data) {
      state.clusterData = data
    },
    setJustClusterData(state, data) {
      state.justClusterData = data
    }
  },
  actions: {
    async fetchClusterData(context) {
      const { data } = await getClusters()
      console.log('data', data)
      const RData = {}
      for (let key in data){
        RData[key] = data[key].cluster
      }
      context.commit('setClusterData', data)
      context.commit('setJustClusterData', RData)
    }
  },
  getters: {
    getClusterData(state) {
      return state.clusterData
    },
    getJustClusterData(state) {
      return state.justClusterData
    }
  }
})