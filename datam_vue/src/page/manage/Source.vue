<template>
  <div>
    <!-- table 展示机器的状态 -->
    <div style="margin-top: 20px">
      <el-button @click="dialogFormVisible = true" size="mini">新增数据库</el-button>
    </div>
    <div>
      <el-table
        :data="tableData.filter(data => !search || data.db_type.toLowerCase().includes(search.toLowerCase()))"
        style="width: 100%">
        <el-table-column type="index" width="50"></el-table-column>
        <el-table-column property="db_type" label="数据库类型" width="120"></el-table-column>
        <el-table-column property="host" label="数据库地址" width="240"></el-table-column>
        <el-table-column property="describe" label="描述" width="240"></el-table-column>
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
              @click="openEdit(scope.$index, scope.row)">编辑
            </el-button>
            <el-button
              size="mini"
              type="danger"
              @click="deleteSource(scope.$index, scope.row)">删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div>
      <!-- Form -->
      <el-dialog title="新增数据源配置" :visible.sync="dialogFormVisible">
        <el-form :model="form">
          <el-form-item label="数据库类型" :label-width="formLabelWidth">
            <el-select v-model="form.db_type" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="描述" :label-width="formLabelWidth">
            <el-input v-model="form.describe" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="主机地址" :label-width="formLabelWidth">
            <el-input v-model="form.host" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="主机端口" :label-width="formLabelWidth">
            <el-input v-model="form.port" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="数据库" :label-width="formLabelWidth">
            <el-input v-model="form.database" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="form.user" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="form.password" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="addSource">确 定</el-button>
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
          <el-form-item label="数据库类型" :label-width="formLabelWidth">
            <el-select v-model="editFormData.db_type" placeholder="请选择">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="描述" :label-width="formLabelWidth">
            <el-input v-model="editFormData.describe" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="主机地址" :label-width="formLabelWidth">
            <el-input v-model="editFormData.host" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="主机端口" :label-width="formLabelWidth">
            <el-input v-model="editFormData.port" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="数据库" :label-width="formLabelWidth">
            <el-input v-model="editFormData.database" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="用户名" :label-width="formLabelWidth">
            <el-input v-model="editFormData.user" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="密码" :label-width="formLabelWidth">
            <el-input v-model="editFormData.password" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editFormVisible = false">取消</el-button>
          <el-button type="primary" @click="updateSource">更新</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import api from '../../api/source'

export default {
  data () {
    return {
      options: [{
        value: 'MySQL',
        label: 'MySQL'
      }, {
        value: 'Hive',
        label: 'Hive'
      }],
      tableData: [],
      currentRow: null,

      dialogTableVisible: false,
      dialogFormVisible: false,

      editFormVisible: false, // 默认不显示编辑弹层
      editFormData: {}, // 默认不显示编辑弹层

      form: {
        db_type: '',
        describe: '',
        host: '',
        port: '',
        database: '',
        user: '',
        password: ''
      },
      formLabelWidth: '120px',
      search: ''
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getSource()
  },
  methods: {
    // 删除确认框
    deleteSource (index, row) {
      this.$alert('会删除外键所关联的数据', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        callback: action => {
          if (action === 'confirm') {
            // 删除代码
            api.sourceDel(row).then((response) => {
              this.getSource()
              // 消息提示
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
    // 打开编辑框
    openEdit (index, row) {
      this.editFormVisible = true
      this.editFormData = Object.assign({}, row) // 这句是关键
    },
    getSource () {
      // 发起get请求
      api.sourceList().then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.tableData = response.data
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    },
    // 添加source
    addSource () {
      this.dialogFormVisible = false
      api.sourceAdd(this.form).then((response) => {
        this.getSource()
      }).catch((error) => {
        console.log(error)
      })
    },
    // 点击更新
    updateSource () {
      // 这里再向后台发个post请求重新渲染表格数据
      this.editFormVisible = false
      api.sourceUpdate(this.editFormData).then((response) => {
        this.getSource()
      }).catch((error) => {
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>

</style>
