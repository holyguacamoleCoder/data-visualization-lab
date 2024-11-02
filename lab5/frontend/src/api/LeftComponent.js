import request from '@/utils/request'
import Qs from 'qs'

// 获取雷达视图组数据
export const getRadarData = (params) => {
  return request.get('/trafficI/profile',{
    params,
    paramsSerializer: params => {
      return Qs.stringify(params, {arrayFormat: 'repeat'})
    }
  })
}