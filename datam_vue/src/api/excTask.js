import instance from '../axios'

export default {
  // 获取数据库配置列表
  taskConfList () {
    return instance.get('/api/v1/exec_task/')
  },
  // 新增数据库配置列表
  taskConfAdd (TaskId, UserId, cronData) {
    var data = {
      'task_id': TaskId,
      'user_list': UserId,
      'cron_data': cronData
    }
    return instance.post('/api/v1/exec_task/', data)
  },
  // 删除数据库配置列表
  taskConfDel (data) {
    return instance.delete('/api/v1/exec_task/' + data.id + '/')
  },
  // 更新数据库配置列表
  taskConfUpdate (data) {
    return instance.put('/api/v1/exec_task/' + data.id + '/', data)
  }
}
