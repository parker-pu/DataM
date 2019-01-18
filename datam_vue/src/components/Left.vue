<template id="left">
  <!-- 左边 -->
  <div>
    <el-menu default-active="/"
             class="el-menu-vertical-demo"
             @open="handleOpen"
             @close="handleClose"
             :collapse="isCollapse" router>
      <el-menu-item index="">
        <i class="el-icon-arrow-right" v-if="isCollapse" @click="openLeft"></i>
        <i class="el-icon-arrow-left" v-else @click="closeLeft"></i>
      </el-menu-item>
      <el-menu-item index="/user">
        <i class="iconfont">&nbsp;&#xeb8a;&nbsp;</i>&nbsp;
        <span slot="title">用户</span>
      </el-menu-item>
      <el-menu-item index="/file">
        <i class="el-icon-document"></i>
        <span slot="title">附件信息</span>
      </el-menu-item>
    </el-menu>
  </div>

</template>

<script>
export default {
  data () {
    return {
      isCollapse: true
    }
  },
  methods: {
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    },
    closeLeft () {
      this.isCollapse = true
      this.$emit('listenToChildEvent', this.isCollapse)
    },
    openLeft () {
      this.isCollapse = false
      this.$emit('listenToChildEvent', this.isCollapse)
    }
  }
}
</script>

<style>
  .el-menu-vertical-demo {
    position: absolute;
    left: 0px;
  }
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 150px;
    min-height: 250px;
  }
</style>

<style scoped>

</style>
