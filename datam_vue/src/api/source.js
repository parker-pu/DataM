import instance from '../axios'

export default {
  // 获取数据库配置列表
  sourceList () {
    return instance.get('/api/v1/db_source/')
  },
  // 新增数据库配置列表
  sourceAdd (data) {
    return instance.post('/api/v1/db_source/', data)
  },
  // 删除数据库配置列表
  sourceDel (data) {
    return instance.delete('/api/v1/db_source/' + data.id + '/')
  },
  // 更新数据库配置列表
  sourceUpdate (data) {
    return instance.put('/api/v1/db_source/' + data.id + '/', data)
  }
}
