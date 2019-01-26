<template id="header">
  <div>
    <el-row class="container">
      <!--头部-->
      <el-col :span="24" class="topbar-wrap">
        <!--图标-->
        <div class="topbar-logo topbar-btn">
          <img :src="imgUrl" style="padding-left:4px;">
        </div>
        <!--选项-->
        <div class="topbar-logos">
          <span style="color: #fff;">数据打包</span>
        </div>
        <!-- 中间的部分 -->
        <div class="topbar-title">
          <el-row>
            <!-- 注意：这里就是topNavState作用之处，根据当前路由所在根路由的type值判断显示不同顶部导航菜单 -->
            <el-col :span="24">
              <el-menu class="el-menu-demo" mode="horizontal"
                       @select="handleSelect" :router="true">
                <el-menu-item index="/task">查看任务</el-menu-item>
                <el-menu-item index="/add_task">添加任务</el-menu-item>
                <el-menu-item index="/conf_task">配置任务</el-menu-item>
                <el-menu-item index="/periodic-task">调度</el-menu-item>
                <el-menu-item index="/source">数据源</el-menu-item>
                <el-menu-item index="/log_task">运行记录</el-menu-item>
              </el-menu>
            </el-col>
          </el-row>
        </div>
        <!--最右侧-->
        <div class="topbar-account topbar-btn">
          <el-dropdown trigger="click">
          <span class="el-dropdown-link userinfo-inner">
            <i class="iconfont icon-user"></i> {{userInfo.username}}   <i class="el-icon-caret-bottom"></i></span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item divided @click.native="goUserInfo">
                <div><span style="color: #555;font-size: 14px;">个人信息</span></div>
              </el-dropdown-item>
              <el-dropdown-item>
                <div><span style="color: #555;font-size: 14px;">修改密码</span></div>
              </el-dropdown-item>
              <el-dropdown-item divided @click.native="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-col>
    </el-row>
    <div>
      <el-dialog title="个人信息"
                 :visible.sync="openUserInfo"
                 :close-on-click-modal="false">
        <el-form :model="seeUserInfo"
                 label-width="100px">
          <el-form-item label="用户名：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.username }}</span>
          </el-form-item>
          <el-form-item label="用户状态：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.is_active }}</span>
          </el-form-item>
          <el-form-item :formatter="dateFormat" label="最近登录：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.last_login }}</span>
          </el-form-item>
          <el-form-item label="超级用户：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.is_superuser }}</span>
          </el-form-item>
          <el-form-item label="姓：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.first_name }}</span>
          </el-form-item>
          <el-form-item label="名：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.last_name }}</span>
          </el-form-item>
          <el-form-item label="邮箱：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.email }}</span>
          </el-form-item>
          <el-form-item :formatter="dateFormat" label="创建时间：" :label-width="seeWidth">
            <span style="float: left">{{ seeUserInfo.date_joined }}</span>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import store from '../store/index'
import apiToken from '../api/login'
import moment from 'moment'

export default {
  store,
  data () {
    return {
      activeName: 'first',
      imgUrl: require('../assets/logo.png'),
      defaultActiveIndex: '/',
      loading: false,
      userInfo: {},
      openUserInfo: false,
      seeUserInfo: {},
      seeWidth: '120px'
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getUserInfo()
  },
  methods: {
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
    },
    // 时间格式化
    dateFormat (row, column) {
      let date = row[column.property]
      if (date === undefined) {
        return ''
      }
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    goUserInfo () {
      this.seeUserInfo = this.userInfo
      this.openUserInfo = true
    },
    getUserInfo () {
      // 发起get请求
      apiToken.tokenUserInfo().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.userInfo = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    logout () {
      // 清除token
      this.$store.dispatch('UserLogout')
      if (!this.$store.state.token) {
        this.$router.push('/login')
        this.$message({
          type: 'success',
          message: '登出成功'
        })
      } else {
        this.$message({
          type: 'info',
          message: '登出失败'
        })
      }
    }
  }
}
</script>

<style>
</style>

<style scoped>
  html {
    font-size: 14px;
  }

  @media all and (max-width: 768px) {
    html {
      font-size: 12px;
    }
  }

  a {
    text-decoration: none;
  }

  ul {
    list-style: none;
    margin-bottom: 0;
  }

  .container {
    position: absolute;
    left: 0px;
    width: 100%;
  }

  /* top navbar style start */
  .container .topbar-wrap {
    height: 60px;
    line-height: 60px;
    background: #373d41;
    padding: 0px;
  }

  .container .topbar-wrap .topbar-btn {
    color: #fff;
  }

  .container .topbar-wrap .topbar-logo {
    float: left;
    width: 60px;
    line-height: 60px;
  }

  .container .topbar-wrap .topbar-logos {
    float: left;
    width: 128px;
    line-height: 60px;
    font-size: 14px;
  }

  /* 设置图片的位置 */
  .container .topbar-wrap .topbar-logo img, .container .topbar-wrap .topbar-logos img {
    height: 60px;
    margin-top: 2px;
    margin-left: 2px;
  }

  .container .topbar-wrap .topbar-title {
    float: left;
    ext-align: left;
    padding-left: 10px;
    border-left: 1px solid #000;
  }

  .topbar-title .el-menu--horizontal {
    background-color: transparent;
  }

  .el-menu--horizontal > .el-menu-item:not(.is-disabled):hover, .el-menu--horizontal > .el-menu-item:not(.is-disabled):focus, .el-menu--horizontal > .el-menu-item.is-active {
    color: #fff;
    background-color: transparent;
    border-bottom: 2px solid #409EFF !important;
  }

  .topbar-title .el-menu--horizontal > .el-menu-item {
    height: 60px;
    line-height: 60px;
    width: 100px;
    color: #fff;
  }

  .el-menu-item .iconfont {
    margin-right: 5px;
    display: inline-block;
    width: 24px;
    text-align: center;
    font-size: 18px;
    vertical-align: middle;
  }

  .container .topbar-wrap .topbar-account {
    float: right;
    padding-right: 12px;
  }

  .container .topbar-wrap .topbar-left {
    float: left;
    padding-left: 12px;
  }

  .container .topbar-wrap .topbar-timer {
    display: inline-block;
  }

  .container .topbar-wrap .topbar-timer span {
    display: inline-block;
    vertical-align: middle;
  }

  .container .topbar-wrap .topbar-timer .login-name {
    margin: 0 6px;
    font-style: normal;
  }

  .container .topbar-wrap .userinfo-inner {
    cursor: pointer;
    color: #fff;
    padding-left: 10px;
  }

  .container .topbar-wrap .userinfo-inner img {
    margin-left: 6px;
    width: 40px;
    height: 60px;
    border: 1px solid #504d4d;
    -webkit-border-radius: 50%;
    -moz-border-radius: 50%;
    border-radius: 50%;
    vertical-align: middle;
  }

  /* top navbar style end */

  /* left sidebar style start */
  .container aside {
    min-width: 50px;
    background: #333744;
  }

  .container aside::-webkit-scrollbar {
    display: none;
  }

  .container aside .menu-toggle {
    background: #4A5064;
    text-align: center;
    color: white;
    height: 60px;
    line-height: 60px;
  }

  .container aside .menu-toggle .iconfont:hover {
    cursor: pointer;
  }

  aside .el-menu-item, aside .el-submenu__title {
    color: #fff;
    text-align: left;
  }

  aside .el-menu-item:hover, aside .el-submenu .el-menu-item:hover, aside .el-submenu__title:hover {
    background-color: #7ed2df;
  }

  aside .el-submenu .el-menu-item {
    background-color: #333744;
  }

  aside .el-submenu .el-menu-item:hover {
    background-color: #4A5064;
  }

  aside .el-submenu .el-menu-item.is-active, aside .el-menu-item.is-active,
  aside .el-submenu .el-menu-item.is-active:hover, aside .el-menu-item.is-active:hover {
    background-color: #00C1DE;
    color: #fff;
  }

  .container aside.showSidebar {
    overflow-x: hidden;
    overflow-y: auto;
  }

  .container aside .el-menu {
    height: 100%; /*写给不支持calc()的浏览器*/
    height: calc(100% - 80px);
    border-radius: 0px;
    background-color: #333744;
    border-right: 0px;
  }

  .container aside .el-submenu .el-menu-item {
    min-width: 60px;
  }

  .container aside .el-menu {
    width: 189px;
  }

  .container aside .el-menu--collapse {
    width: 60px;
  }

  .container aside .el-menu .el-menu-item, .container aside .el-submenu .el-submenu__title {
    height: 60px;
    line-height: 60px;
  }

  .container aside .el-menu-item:hover, .container aside .el-submenu .el-menu-item:hover, .container aside .el-submenu__title:hover {
    background-color: #7ed2df;
  }

  /* left sidebar style end */

  .container .main {
    display: -ms-flexbox;
    display: flex;
    position: absolute;
    top: 50px;
    bottom: 0px;
    overflow: hidden;
  }

  .container .warp-main {
    padding-top: 10px;
    padding-bottom: 10px;
  }

  .container .content-container {
    background: #f2f2f2;
    -ms-flex: 1;
    flex: 1;
    overflow-y: auto;
    padding: 10px;
  }

  .container .content-container .content-wrapper {
    background-color: #fff;
    box-sizing: border-box;
  }

  .grid-content .toolbar {
    padding: 10px 10px 0 10px;
  }

  .grid-content .el-pagination {
    padding: 15px;
    text-align: right;
  }

  .footer .footer-msg {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    font-size: 1.08rem;
    color: #666;
  }

  .footer .footer-msg a {
    color: #428bca;
    text-decoration: none;
  }

  .footer .footer-msg a:hover,
  .footer .footer-msg a:focus,
  .footer .footer-msg a:active {
    color: #2a6496;
    text-decoration: underline;
    outline: 0;
  }

  /* bottom footer style end */

  /* scrollbar style start */
  ::-webkit-scrollbar {
    background: transparent;
    width: 10px;
    height: 10px
  }

  ::-webkit-scrollbar-thumb {
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    background-color: #e1e1e1;
    width: 6px;
    height: 6px;
    border: 2px solid transparent;
    background-clip: content-box
  }

  ::-webkit-scrollbar-track {
    -webkit-border-radius: 5px;
    -moz-border-radius: 5px;
    border-radius: 5px;
    background-color: #fafafa
  }
</style>
