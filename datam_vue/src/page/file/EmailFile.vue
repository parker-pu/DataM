<template>
  <div>
    <!-- table 展示机器的状态 -->
    <div>
      <el-table
        :data="tableData.filter(data => !search || data.task_name.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">
        <el-table-column property="task_uuid" label="任务id" width="320"></el-table-column>
        <el-table-column property="task_name" label="任务名" width="200"></el-table-column>
        <el-table-column :formatter="dateFormat" property="insert_time" label="完成时间" width="155">
        </el-table-column>
        <el-table-column property="username" label="接收用户" width="100"></el-table-column>
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
              @click="downFile(scope.$index, scope.row)">下载附件
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deleteFile(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import apiFile from '../../api/file'
import moment from 'moment'

export default {
  data () {
    return {
      tableData: [],
      search: ''
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getEmailFile() // 获取日志数据列表
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
    getEmailFile () {
      // 发起get请求
      apiFile.fileList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.tableData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    // 下载文件
    downFile (index, row) {
      window.location.href = row.file_path
    },
    // 删除文件
    deleteFile (index, row) {
      this.$alert('是否确认删除', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        callback: action => {
          if (action === 'confirm') {
            // 删除任务代码
            apiFile.fileDel(row).then((response) => {
              this.getEmailFile()
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
</style>
