<template>
  <div>
    <el-container>
      <el-header>
        <Header></Header>
      </el-header>
      <el-container>
        <el-aside :width="leftSize">
          <Left v-on:listenToChildEvent="updateLeft"></Left>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from '../components/Header'
import Left from '../components/Left'

export default {
  name: 'Main',
  components: {
    Header,
    Left
  },
  data () {
    return {
      leftSize: '65px'
    }
  },
  methods: {
    updateLeft (isCollapse) {
      if (isCollapse === true) {
        this.leftSize = '65px'
      } else {
        this.leftSize = '151px'
      }
    }
  }
}
</script>

<style scoped>
</style>
