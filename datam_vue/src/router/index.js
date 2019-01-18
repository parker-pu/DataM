import Vue from 'vue'
import Router from 'vue-router'
import Login from '../page/login/Login'
import store from '../store/index.js'
import User from '../page/user/User'
import Task from '../page/task/Task'
import Source from '../page/manage/Source'
import AddTask from '../page/task/AddTask'
import Main from '../page/Main'
import ConfTask from '../page/task/ConfTask'
import LogTask from '../page/task/LogTask'
import EmailFile from '../page/file/EmailFile'
import PeriodicTask from '../page/task/PeriodicTask'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Main',
      component: Main,
      redirect: '/task',
      meta: {
        requiresAuth: true
      },
      children: [
        // 用户
        {
          path: '/user',
          name: 'user',
          component: User,
          meta: {
            requiresAuth: true
          }
        },
        // 文件
        {
          path: '/file',
          name: 'file',
          component: EmailFile,
          meta: {
            requiresAuth: true
          }
        },
        {
          path: '/task',
          name: 'task',
          component: Task,
          meta: {
            requiresAuth: true
          }
        },
        // 添加任务
        {
          path: '/add_task',
          name: 'AddTask',
          component: AddTask,
          meta: {
            requiresAuth: true
          }
        },
        // 配置任务
        {
          path: '/conf_task',
          name: 'ConfTask',
          component: ConfTask,
          meta: {
            requiresAuth: true
          }
        },
        // 任务日志
        {
          path: '/log_task',
          name: 'LogTask',
          component: LogTask,
          meta: {
            requiresAuth: true
          }
        },
        // 数据源
        {
          path: '/source',
          name: 'source',
          component: Source,
          meta: {
            requiresAuth: true
          }
        },
        // 定时任务
        {
          path: '/periodic-task',
          name: 'PeriodicTask',
          component: PeriodicTask,
          meta: {
            requiresAuth: true
          }
        }
      ]
    }
  ]
})

// 注册全局钩子用来拦截导航
router.beforeEach((to, from, next) => {
  // 获取store里面的token
  let token = store.state.token
  // 判断要去的路由有没有requiresAuth
  if (to.meta.requiresAuth) {
    if (token) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
        // 将刚刚要去的路由path（却无权限）作为参数，方便登录成功后直接跳转到该路由
      })
    }
  } else {
    next()// 如果无需token,那么随它去吧
  }
})

export default router
