<template>
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
      <!-- 侧边栏 -->
      <el-aside width="200px">
        <!-- 侧边栏菜单区域  default-active="1"没写-->
        <el-menu background-color="#fff" text-color="#535353" active-text-color="#409eff" router>
          <!-- 新建按钮 -->
          <el-menu-item index="0">
            <el-button size="midium" @click="newFile" type="primary" plain>新建文档</el-button>
          </el-menu-item>
          <!-- 不分级菜单 -->
          <el-menu-item index="1">
            <i class="fa fa-archive" style="padding: 0 10px 0 10px"></i>
            <span slot="title">工作台</span>
          </el-menu-item>
          <!-- 不分级菜单 -->
          <el-menu-item index="2">
            <i class="fa fa-envelope-o" style="padding: 0 10px 0 10px"></i>
            <span slot="title">收件箱</span>
          </el-menu-item>
          <!-- 分割线 -->
          <div style="margin: 8px 20px; height: 1.5px; background-color: rgb(230, 230, 230);"></div>
          <!-- 不分级菜单 -->
          <el-menu-item index="3">
            <i class="fa fa-desktop" style="padding: 0 10px 0 10px"></i>
            <span slot="title">我的桌面</span>
          </el-menu-item>
          <!-- 一级菜单 -->
          <el-submenu index="4">
            <!-- 一级菜单模板区域 -->
            <template slot="title">
              <!-- 图标 -->
              <i class="fa fa-cube" style="padding: 0 10px 0 10px"></i>
              <!-- 文本 -->
              <span>团队空间</span>
            </template>
            <!-- 二级菜单 -->
            <el-menu-item index="4-1">
              <template slot="title">
                <!-- 图标 -->
                <!-- <i class="el-icon-location"></i> -->
                <!-- 文本 -->
                <span >团队名称1</span>
              </template>
            </el-menu-item>
            <el-menu-item index="4-2">
              <template slot="title">
                <!-- 图标 -->
                <!-- <i class="el-icon-location"></i> -->
                <!-- 文本 -->
                <span>团队名称2</span>
              </template>
            </el-menu-item>
          </el-submenu>
          <!-- 不分级菜单 -->
          <el-menu-item index="5">
            <i class="fa fa-trash-o" style="padding: 0 12px 0 11px"></i>
            <span slot="title">回收站</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!-- 右侧内容主体 -->
      <el-main>
        <!-- 路由占位符 -->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  methods: {
    logout() {
      window.sessionStorage.clear();
      this.$router.push("/login");
    },
    changeInfo() {
      window.sessionStorage.clear();
      this.$router.push("/myinfo");
    },
    newFile() {
      window.sessionStorage.clear();
      this.$router.push("/editor");
    },
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
  align-items: center;
}

.el-aside {
  padding-top: 30px;
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
  align-items: center;
}
.el-avatar {
  margin: 10px 15px 10px 30px;
}
.site-name {
  font-size: 30px;
  color: #409eff;
}
.head-box3 {
  display: flex;
  align-items: center;
  // 居右对齐
  justify-content: flex-end;
}

// .bg-purple {
//   background: #d3dce6;
// }
// .bg-purple-light {
//   background: #e5e9f2;
// }
// .grid-content {
//   border-radius: 4px;
//   max-height: 30px;
// }
.row-bg {
  align-items: center;
  // margin: 2.5px 0;
  // background-color: #f9fafc;
}
</style>
