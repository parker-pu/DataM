<template>
  <div>
    <div>
      <el-steps :active="active" finish-status="success" style="margin-top: 10px" simple>
        <el-step title="任务描述" description="输入任务的一些信息" icon="el-icon-edit-outline"></el-step>
        <el-step title="选择数据库" description="选择任务需要的数据库信息" icon="el-icon-news"></el-step>
        <el-step title="执行语句" description="输入需要执行的语句" icon="el-icon-loading"></el-step>
      </el-steps>
    </div>
    <div class="fromDiv">
      <el-form :model="editFormData"
               label-width="80px"
               :rules="rules"
               ref="editForm">
        <div class="TaskEdit" v-if="active === 0">
          <el-form-item></el-form-item>
          <el-form-item>
            <el-col :span="13">
              <el-form-item label="名称：" prop="name">
                <el-input v-model="editFormData.name" autocomplete="off"></el-input>
              </el-form-item>
            </el-col>
            <el-col class="line" :span="2">
              <i class="el-icon-edit"></i>
            </el-col>
            <el-col :span="7">
              <el-form-item label="状态：">
                <el-radio-group v-model="editFormData.task_status">
                  <el-radio-button label="true"></el-radio-button>
                  <el-radio-button label="false"></el-radio-button>
                </el-radio-group>
              </el-form-item>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-col :span="24">
              <el-form-item label="描述：" prop="describe">
                <el-input
                  type="textarea"
                  :autosize="{ minRows: 4, maxRows: 10}"
                  placeholder="请输入内容"
                  v-model="editFormData.describe">
                </el-input>
              </el-form-item>
            </el-col>
          </el-form-item>
        </div>
        <div class="Source" v-if="active === 1">
          <el-form-item></el-form-item>
          <el-form-item>
            <el-col :span="24">
              <el-form-item label="数据源：" prop="db_source">
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
            </el-col>
          </el-form-item>
        </div>
        <div class="ExecCode" v-if="active === 2">
          <el-form-item prop="code_context">
            <monaco-editor class="editor" v-model="editFormData.code_context" language="sql">
            </monaco-editor>
            <el-button-group>
              <el-button type="primary" @click="format" icon="el-icon-edit">代码格式化</el-button>
              <el-button type="primary" @click="cleanCode" icon="el-icon-delete">清空代码</el-button>
            </el-button-group>
          </el-form-item>
          <el-form-item label="">
          </el-form-item>
        </div>
      </el-form>
    </div>
    <div class="submitDiv">
      <el-button style="margin-top: 12px;" @click="prev" v-if="active === 1||active === 2">上一步</el-button>
      <el-button style="margin-top: 12px;" @click="next" v-if="active === 0||active === 1">下一步</el-button>
      <el-button style="margin-top: 12px;" @click="addTask" v-if="active === 2">提交任务</el-button>
    </div>
  </div>
</template>

<script>
import MonacoEditor from 'vue-monaco'
import sqlFormatter from 'sql-formatter'
import apiSource from '../../api/source'
import apiTask from '../../api/task'

export default {
  components: {
    MonacoEditor
  },

  data () {
    return {
      active: 0,
      formLabelWidth: '120px',
      editFormData: {
        task_status: true
      },
      db_source_list: null,
      rules: { // 验证规则
        name: [
          {required: true, message: '缺少任务名', trigger: 'blur'}
        ],
        describe: [
          {required: true, message: '缺少描述', trigger: 'blur'}
        ],
        db_source: [
          {required: true, message: '缺少数据库', trigger: 'blur'}
        ],
        code_context: [
          {required: true, message: '缺少数据库', trigger: 'blur'}
        ]
      }
    }
  },
  // 在页面加载的时候，调这个函数
  mounted: function () {
    this.getDBSource()
  },
  methods: {
    // 上一步
    prev () {
      if (this.active-- < 0) this.active = 0
    },
    // 下一步
    next () {
      if (this.active++ > 2) this.active = 2
    },
    format () {
      /* 格式化代码 */
      this.editFormData.code_context = sqlFormatter.format(this.editFormData.code_context)
    },
    cleanCode () {
      this.editFormData.code_context = ''
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
    addTask () {
      apiTask.taskAdd(this.editFormData).then((response) => {
        // then 指成功之后的回调 (注意：使用箭头函数，可以不考虑this指向)
        this.$notify({
          title: '成功',
          message: '添加任务成功',
          type: 'success'
        })
        this.$router.push({path: '/task'})
      }).catch((error) => {
        // catch 指请求出错的处理
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>
  .fromDiv {
    height: 400px;
  }

  .editor {
    height: 340px;
  }

  .submitDiv {
    width: 200px;
    margin: 0 auto;
  }
  .ExecCode {
    position: relative;
    top: 5px;
    height: 400px;
  }
</style>
