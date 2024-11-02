import request from '@/utils/request'

// 获取周视图相关数据
export const getMapData = () => {
  return request.get('/maps', {
    params:{
    }
  })
}

export const getTrafficData = (params) => {
  return request.get('/trafficI/time_range', {
    params
  })
}