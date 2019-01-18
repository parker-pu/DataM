import instance from '../axios'

export default {
  // 获取数据库配置列表
  fileList () {
    return instance.get('/api/v1/file/')
  },
  // 删除数据库配置列表
  fileDel (data) {
    return instance.delete('/api/v1/file/' + data.id)
  }
}
