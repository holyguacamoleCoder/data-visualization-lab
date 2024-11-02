import request from '@/utils/request'
import Qs from 'qs'
// 获取车辆视图组数据
export const getProcessByIds = (params) => {
  return request.get('/trafficI/process_by_ids',{
    params,
    paramsSerializer: params => {
      return Qs.stringify(params, {arrayFormat: 'repeat'})
    }
  })
}