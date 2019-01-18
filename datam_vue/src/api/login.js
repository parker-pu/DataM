import instance from '../axios'

export default {
  // 用户注册
  userRegister (data) {
    return instance.post('/api-token-auth/', data)
  },
  // 用户登录
  userLogin (data) {
    return instance.post('/api-token-auth/', data)
  },
  // 根据 token 获取 User 的信息
  tokenUserInfo () {
    return instance.post('/api-token-auth/')
  }
}
