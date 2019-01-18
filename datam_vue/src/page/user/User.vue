<template>
  <div>
    <!-- table 展示机器的状态 -->
    <div style="margin-top: 20px">
      <el-button @click="dialogFormVisible = true" size="mini">新增用户</el-button>
    </div>
    <div>
      <el-table
        :data="tableData.filter(data => !search || data.username.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column property="username" label="用户名" width="120"></el-table-column>
        <el-table-column property="email" label="邮箱" width="240"></el-table-column>
        <el-table-column property="is_staff" label="是否活跃" width="120"></el-table-column>
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
              @click="editUser(scope.$index, scope.row)">编辑
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deleteUser(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <!-- Form -->
      <el-dialog title="新增用户" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="form.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="form.password" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" :label-width="formLabelWidth">
            <el-input v-model="form.email" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="addUser">确 定</el-button>
        </div>
      </el-dialog>
    </div>
    <div>
      <el-dialog title="编辑"
                 :visible.sync="editFormVisible"
                 :close-on-click-modal="false"
                 class="edit-form">
        <el-form :model="editFormData"
                 label-width="80px"
                 ref="editForm">
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="editFormData.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="editFormData.password" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" :label-width="formLabelWidth">
            <el-input v-model="editFormData.email" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click="updateUser">更新</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import apiUser from '../../api/user'

export default {
  // name: 'Main',
  data () {
    return {
      tableData: [],
      dialogFormVisible: false,

      editFormVisible: false, // 默认不显示编辑弹层
      editFormData: {}, // 默认不显示编辑弹层

      form: {
        username: '',
        password: '',
        email: ''
      },
      formLabelWidth: '120px',
      search: ''
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getUser()
  },
  methods: {
    editUser (index, row) {
      this.editFormVisible = true
      this.editFormData = Object.assign({}, row) // 这句是关键
    },
    // 删除用户
    deleteUser (index, row) {
      this.$alert('是否确认删除', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        callback: action => {
          if (action === 'confirm') {
            // 删除任务代码
            apiUser.userDel(row).then((response) => {
              this.getUser()
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
    getUser () {
      // 发起get请求
      apiUser.userList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.tableData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    // 增加用户
    addUser () {
      this.dialogFormVisible = false
      apiUser.userAdd(this.form).then((response) => {
        this.getUser()
      }).catch((error) => {
        console.log(error)
      })
    },
    // 更新用户
    updateUser () {
      // 这里再向后台发个post请求重新渲染表格数据
      this.editFormVisible = false
      apiUser.userUpdate(this.editFormData).then((response) => {
        this.getUser()
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>

</style>
