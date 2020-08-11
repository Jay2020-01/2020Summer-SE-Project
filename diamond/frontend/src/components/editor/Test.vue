<template>
  <div>
    <el-container class="home-container">
      <!-- 头部区域 -->
      <el-header height="60px" direction="horizontal">
        <el-row type="flex" class="row-bg">
          <el-col :span="6" :offset="0">
            <div class="grid-content head-box1 bg-purple">
              <!-- 头像区域 -->
              <el-avatar icon="fa fa-diamond" :size="40">logo</el-avatar>
              <span class="site-name">钻石文档</span>
            </div>
          </el-col>
          <el-col :span="5" :offset="7">
            <div class="grid-content head-box2 bg-purple-light">
              <el-input placeholder="搜索内容" v-model="input" size="small" clearable></el-input>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="grid-content head-box3 bg-purple">
              <div>
                <el-button size="small" @click="changeInfo">修改信息</el-button>
                <el-button size="small" @click="logout">退出</el-button>
                <!-- <el-button size="samll" @click="logout">退出</el-button> -->
              </div>
            </div>
          </el-col>
        </el-row>
      </el-header>
      <!-- 页面主体区域 -->
      <el-container>
        <!-- 右侧内容主体 -->
        <el-main>
          <!-- 路由占位符 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import editor from "./Editor";
export default {
  components: {
    editor,
  },
  data() {
    return {
      content: "",
    };
  },
};
</script>

<style lang="less" scoped>
.home-container {
  height: 100%;
}

.el-header {
  background-color: #ffffff;
  margin-bottom: 7px;
  color: #333;
  text-align: left;
  line-height: 60px;
  border: 1px solid #eee;
  box-shadow: 0 0 10px #ddd;
}

.el-aside {
  padding-top: 40px;
  background-color: #ffffff;
  color: #333;
  text-align: left;
  line-height: 200px;
  border-right: 1px solid #eee;
  .el-menu {
    border-right: none;
  }
}

.el-main {
  background-color: #ffffff;
  color: #333;
  text-align: center;
}

body > .el-container {
  margin-bottom: 40px;
}

// 顶栏内容样式
.head-box1 {
  display: flex;
}
.el-avatar {
  margin: 5px 20px 5px 0;
}
.site-name {
  font-size: 30px;
  color: #409eff;
}
.head-box3 {
  display: flex;
  // 居右对齐
  justify-content: flex-end;
}

// .bg-purple {
//   background: #d3dce6;
// }
// .bg-purple-light {
//   background: #e5e9f2;
// }
.grid-content {
  border-radius: 4px;
  min-height: 60px;
}
.row-bg {
  margin: 5px 0;
  // background-color: #f9fafc;
}
</style>