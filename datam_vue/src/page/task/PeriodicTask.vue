<template>
  <div>
    <!-- table 展示机器的状态 -->
    <div>
      <el-table
        :data="PeriodicTaskData.filter(data => !search ||
        data.name.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">
        <el-table-column property="uuid" label="#id" width="320"></el-table-column>
        <el-table-column property="name" label="任务名" width="200"></el-table-column>
        <el-table-column :formatter="booleFormat" property="enabled" label="激活" width="100">
        </el-table-column>
        <el-table-column property="total_run_count" label="运行次数" width="100"></el-table-column>
        <el-table-column property="cron" label="定时配置" width="200"></el-table-column>
        <el-table-column :formatter="dateFormat" property="date_changed" label="更新时间" width="200">
        </el-table-column>
        <el-table-column property="description" label="任务描述"></el-table-column>
        <el-table-column
          align="right">
          <template slot="header" slot-scope="scope">
            <el-input
              v-model="search"
              size="mini"
              placeholder="输入关键字搜索"/>
          </template>
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="editPeriodicTask(scope.$index, scope.row)">详细
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deletePeriodicTask(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-dialog title="详细"
                 :visible.sync="checkPeriodicTask"
                 :close-on-click-modal="false">
        <el-form :model="PeriodicTaskInfo">
          <el-form-item label="任务名：" :label-width="labelWidth">
            <span style="float: left">{{ PeriodicTaskInfo.name }}</span>
          </el-form-item>
          <el-form-item label="定时配置：" :label-width="labelWidth">
            <span style="float: left">{{ PeriodicTaskInfo.cron }}</span>
          </el-form-item>
          <el-form-item :formatter="dateFormat" label="更新时间：" :label-width="labelWidth">
            <span style="float: left">{{ PeriodicTaskInfo.date_changed }}</span>
          </el-form-item>
          <el-form-item label="数据：" :label-width="labelWidth">
            <span style="float: left">{{ PeriodicTaskInfo.args }}</span>
          </el-form-item>
          <el-form-item label="任务描述：" :label-width="labelWidth">
            <span style="float: left">{{ PeriodicTaskInfo.description }}</span>
          </el-form-item>
        </el-form>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import apiTask from '../../api/task'
import moment from 'moment'

export default {
  // name: 'PeriodicTask',
  data () {
    return {
      PeriodicTaskData: [],
      search: '',
      checkPeriodicTask: false,
      PeriodicTaskInfo: {},
      labelWidth: '120px'
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getPeriodicTask() // 获取定时任务的列表
  },
  methods: {
    // 格式化 boole
    booleFormat (row, column) {
      let v = row[column.property]
      if (v === true) {
        return '是'
      } else {
        return '否'
      }
    },
    // 获取定时运行的任务
    getPeriodicTask () {
      // 发起get请求
      apiTask.periodicTaskList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.PeriodicTaskData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    // 时间格式化
    dateFormat (row, column) {
      let date = row[column.property]
      if (date === undefined) {
        return ''
      }
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    //  删除调度任务
    deletePeriodicTask (index, row) {
      // 发起delete请求
      this.$alert('是否确认删除', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        callback: action => {
          if (action === 'confirm') {
            // 删除任务代码
            apiTask.periodicTaskDel(row).then((response) => {
              this.getPeriodicTask()
              this.$notify({
                title: '成功',
                message: '删除成功',
                type: 'success'
              })
            }).catch((error) => {
              console.log(error)
            })
          }
        }
      })
    },
    // 详细
    editPeriodicTask (index, row) {
      this.checkPeriodicTask = true
      this.PeriodicTaskInfo = row
    }
  }
}
</script>

<style scoped>
</style>
