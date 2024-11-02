import request from '@/utils/request'

// 获取周视图相关数据
export const getProcessByIds = (params) => {
  return request.get('/trafficI/process_by_ids',{
    params
  })
}