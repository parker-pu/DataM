<template>
  <div>
    <!-- table 展示机器的状态 -->
    <div>
      <el-table
        :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column property="name" label="任务名" width="200"></el-table-column>
        <el-table-column :formatter="booleFormat" property="task_status" label="任务状态" width="100"></el-table-column>
        <el-table-column :formatter="dateFormat" property="update_time" label="最近更新" width="160">
        </el-table-column>
        <el-table-column property="describe" label="任务描述"></el-table-column>
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
              @click="editTask(scope.$index, scope.row)">编辑
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deleteTask(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <el-dialog title="编辑任务"
                 :visible.sync="editFormVisible"
                 :close-on-click-modal="false"
                 class="edit-form">
        <el-form :model="editFormData"
                 label-width="80px"
                 ref="editForm">
          <el-form-item label="名称" :label-width="formLabelWidth">
            <el-input v-model="editFormData.name" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="描述" :label-width="formLabelWidth">
            <el-input
              type="textarea"
              :autosize="{ minRows: 4, maxRows: 10}"
              placeholder="请输入内容"
              v-model="editFormData.describe">
            </el-input>
          </el-form-item>
          <el-form-item label="数据源" :label-width="formLabelWidth">
            <el-select v-model="editFormData.db_source_id" placeholder="请选择">
              <el-option
                v-for="item in db_source_list"
                :key="item.id"
                :label="item.host"
                :value="item.id">
                <span style="float: left">{{ item.host }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">{{ item.db_type }}</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label-width="formLabelWidth">
            <monaco-editor class="editor" v-model="editFormData.code_context" language="sql">
            </monaco-editor>
            <el-button-group>
              <el-button type="primary" @click="format" icon="el-icon-edit">代码格式化</el-button>
              <el-button type="primary" @click="cleanCode" icon="el-icon-delete">清空代码</el-button>
            </el-button-group>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click="updateTask">更新</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import apiTask from '../../api/task'
import apiSource from '../../api/source'
import moment from 'moment'
import MonacoEditor from 'vue-monaco'
import sqlFormatter from 'sql-formatter'

export default {
  components: {
    MonacoEditor
  },
  // name: 'Main',
  data () {
    return {
      tableData: [],
      db_source_list: null,

      editFormVisible: false, // 默认不显示编辑弹层
      editFormData: {}, // 默认不显示编辑弹层

      formLabelWidth: '120px',
      search: ''
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getTask() // 获取任务列表
    this.getDBSource() // 获取数据库列表
  },
  methods: {
    format () {
      /* 格式化代码 */
      this.editFormData.code_context = sqlFormatter.format(this.editFormData.code_context)
    },
    cleanCode () {
      this.editFormData.code_context = ''
    },
    // 格式化 boole
    booleFormat (row, column) {
      let v = row[column.property]
      if (v === true) {
        return '活跃'
      } else {
        return '失效'
      }
    },
    getDBSource () {
      // 发起get请求
      apiSource.sourceList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.db_source_list = response.data
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
    // 编辑任务
    editTask (index, row) {
      this.editFormVisible = true
      this.editFormData = Object.assign({}, row) // 这句是关键
    },
    // 删除任务
    deleteTask (index, row) {
      this.$alert('是否确认删除', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        callback: action => {
          if (action === 'confirm') {
            // 删除任务代码
            apiTask.taskDel(row).then((response) => {
              this.getTask()
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
    // 获取任务列表
    getTask () {
      // 发起get请求
      apiTask.taskList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.tableData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    // 点击更新
    updateTask () {
      // 这里再向后台发个post请求重新渲染表格数据
      this.editFormVisible = false
      apiTask.taskUpdate(this.editFormData).then((response) => {
        this.getTask()
      }).catch((error) => {
        console.log(error)
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
