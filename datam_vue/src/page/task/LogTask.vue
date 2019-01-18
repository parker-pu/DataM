<template>
  <div>
    <!-- table 展示机器的状态 -->
    <div>
      <el-table
        :data="tableData.filter(data => !search || data.task_name.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">
        <el-table-column property="task_uuid" label="任务id" width="320"></el-table-column>
        <el-table-column property="task_name" label="任务名" width="200"></el-table-column>
        <el-table-column property="status" label="任务状态" width="100"></el-table-column>
        <el-table-column :formatter="dateFormat" property="date_done" label="完成时间" width="155">
        </el-table-column>
        <el-table-column property="task_describe" label="任务描述"></el-table-column>
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
              @click="infoLog(scope.$index, scope.row)">详细
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deleteTaskLog(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-dialog title="详细"
                 :visible.sync="editFormVisible"
                 :close-on-click-modal="false"
                 class="edit-form">
        <el-form :model="editData"
                 label-width="100px">
          <el-form-item label="任务名：" width="200">
            <span style="float: left">{{ editData.task_name }}</span>
          </el-form-item>
          <el-form-item label="任务状态：" width="100">
            <span style="float: left">{{ editData.status }}</span>
          </el-form-item>
          <el-form-item :formatter="dateFormat" label="完成时间：" width="150">
            <span style="float: left">{{ editData.date_done }}</span>
          </el-form-item>
          <el-form-item label="任务描述：" width="200">
            <span style="float: left">{{ editData.task_describe }}</span>
          </el-form-item>
          <el-form-item label="用户：" width="200">
            <span style="float: left">{{ editData.username }}</span>
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
  // name: 'Main',
  data () {
    return {
      tableData: [],

      editFormVisible: false, // 默认不显示编辑弹层
      editFormData: {}, // 默认不显示编辑弹层
      editData: {},
      search: ''
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getLogTask() // 获取日志数据列表
  },
  methods: {
    // 时间格式化
    dateFormat (row, column) {
      let date = row[column.property]
      if (date === undefined) {
        return ''
      }
      return moment(date).format('YYYY-MM-DD HH:mm:ss')
    },
    getLogTask () {
      // 发起get请求
      apiTask.taskLogList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.tableData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    infoLog (index, row) {
      // 打开选项框
      this.editFormVisible = true
      this.editData = Object.assign({}, row) // 这句是关键
    },
    // 删除任务
    deleteTaskLog (index, row) {
      this.$alert('是否确认删除', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        callback: action => {
          if (action === 'confirm') {
            // 删除任务代码
            apiTask.taskLogDel(row).then((response) => {
              this.getLogTask()
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
    }
  }
}
</script>

<style scoped>
  .editor {
    height: 340px;
  }
</style>
