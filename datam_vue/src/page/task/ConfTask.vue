<template>
  <div>
    <div>
      <el-form label-width="80px">
        <el-form-item>
          <el-col :span="11">
            <el-table
              :data="tasksData.filter(data => !searchTask ||
            data.name.toLowerCase().includes(searchTask.toLowerCase()))"
              style="width: 100%"
              highlight-current-row
              @current-change="currentChangeTask"
              height="500">
              <el-table-column property="name" label="任务名" width="200"></el-table-column>
              <el-table-column
                align="right">
                <template slot="header" slot-scope="scope">
                  <el-input
                    v-model="searchTask"
                    size="mini"
                    placeholder="输入关键字搜索"/>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
          <el-col :span="1">&nbsp;</el-col>
          <el-col :span="10">
            <el-table
              :data="usersData.filter(data => !searchUser ||
            data.username.toLowerCase().includes(searchUser.toLowerCase()))"
              style="width: 100%"
              tooltip-effect="dark"
              @selection-change="selectionChangeUser"
              height="500">
              <el-table-column
                type="selection"
                width="55">
              </el-table-column>
              <el-table-column property="username" label="用户名" width="100"></el-table-column>
              <el-table-column property="email" label="邮箱" width="250"></el-table-column>
              <el-table-column
                align="right">
                <template slot="header" slot-scope="scope">
                  <el-input
                    v-model="searchUser"
                    size="mini"
                    placeholder="搜索"/>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-form-item>
      </el-form>
    </div>
    <div class="submitDiv">
      <el-button style="margin-top: 12px;" @click="confCron">定时器</el-button>
      <el-button style="margin-top: 12px;" @click="submitTaskData">执行任务</el-button>
    </div>
    <div>
      <el-dialog title="配置定时"
                 :visible.sync="editCronVisible"
                 :close-on-click-modal="false"
                 class="edit-form">
        <el-form :data="cronData"
                 label-width="80px"
                 ref="editForm">
          <el-form-item label="分" :label-width="formLabelWidth">
            <el-input v-model="cronData.minute" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="时" :label-width="formLabelWidth">
            <el-input v-model="cronData.hour" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="周" :label-width="formLabelWidth">
            <el-input v-model="cronData.day_of_week" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="月" :label-width="formLabelWidth">
            <el-input v-model="cronData.day_of_month" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="年" :label-width="formLabelWidth">
            <el-input v-model="cronData.month_of_year" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editCronVisible = false">取消</el-button>
          <el-button type="primary" @click="addCronTask">确定</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import apiTask from '../../api/task'
import apiExcTask from '../../api/excTask'
import apiUser from '../../api/user'

export default {
  name: 'ConfTask',
  data () {
    return {
      tasksData: [],
      usersData: [],

      multipleUser: [],
      multipleUserId: [],
      multipleUserIdCron: [],
      selectTaskId: null,

      editCronVisible: false, // 定时配置页面
      cronData: {}, // 定时任务的数据

      formLabelWidth: '120px',
      searchTask: '',
      searchUser: '',
      currentRowTask: null,
      currentRowUser: null
    }
  },
  mounted: function () {
    this.getTask() // 获取任务列表
    this.getUser() // 获取用户信息
  },
  methods: {
    selectionChangeUser (val) {
      this.multipleUser = val
      var userList = []
      for (var i = 0; i < val.length; i++) {
        userList.push(val[i].id)
      }
      this.multipleUserId = userList
    },
    // 获取任务列表
    getTask () {
      // 发起get请求
      apiTask.taskList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.tasksData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    getUser () {
      // 发起get请求
      apiUser.userList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.usersData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    currentChangeTask (val) {
      this.currentRowTask = val
      this.selectTaskId = val.id
    },
    // 提交任务数据
    submitTaskData () {
      // 判断数据
      if (this.multipleUserIdCron.length !== 0) {
        this.multipleUserId = this.multipleUserIdCron
      }
      apiExcTask.taskConfAdd(
        this.selectTaskId,
        this.multipleUserId,
        this.cronData
      ).then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        // (1) 显示结果
        // (2) 跳转相应页面
        this.$notify({
          title: '成功',
          message: response.data.message,
          type: 'success'
        })
        this.$router.push({path: '/log_task'})
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    confCron () {
      this.multipleUserIdCron = this.multipleUserId
      this.editCronVisible = true
    },
    // 增加配置
    addCronTask () {
      this.submitTaskData()
      this.editCronVisible = false
    }
  }
}
</script>

<style scoped>
  .submitDiv {
    width: 200px;
    margin: 0 auto;
  }
</style>
