import instance from '../axios'

export default {
  // 获取数据库配置列表
  taskList () {
    return instance.get('/api/v1/task/')
  },
  // 新增数据库配置列表
  taskAdd (data) {
    return instance.post('/api/v1/task/', data)
  },
  // 删除数据库配置列表
  taskDel (data) {
    return instance.delete('/api/v1/task/' + data.id + '/')
  },
  // 更新数据库配置列表
  taskUpdate (data) {
    return instance.put('/api/v1/task/' + data.id + '/', data)
  },
  // 获取数据库配置列表
  taskLogList () {
    return instance.get('/api/v1/task_log/')
  },
  // 删除数据库配置列表
  taskLogDel (data) {
    return instance.delete('/api/v1/task_log/' + data.id)
  },
  // 查看定时任务
  periodicTaskList () {
    return instance.get('/api/v1/periodic-task/')
  },
  // 查看定时任务
  periodicTaskDel (data) {
    return instance.delete('/api/v1/periodic-task/' + data.id)
  }
}
