import instance from '../axios'

export default {
  // 用户查看
  userList () {
    return instance.get('/api/v1/users/')
  },
  // 新增用户
  userAdd (data) {
    return instance.post('/api/v1/users/', data)
  },
  // 删除用户
  userDel (data) {
    return instance.delete('/api/v1/users/' + data.id + '/')
  },
  // 更新用户
  userUpdate (data) {
    return instance.put('/api/v1/users/' + data.id + '/', data)
  }
}
