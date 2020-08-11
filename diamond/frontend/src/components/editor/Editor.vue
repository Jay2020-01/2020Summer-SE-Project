<template>
  <div>
    <el-container class="home-container">
      <!-- 头部区域 -->
      <el-header height="60px" direction="horizontal">
        <el-row type="flex" class="row-bg">
          <el-col :span="6" :offset="0">
            <div class="grid-content head-box1 bg-purple">
              <!-- 顶部工具栏区域 -->
              <!-- 返回按钮 -->
              <el-tooltip class="item" effect="dark" content="返回" placement="bottom">
                <el-button size="big" icon="fa fa-angle-left" style="border: none;"></el-button>
              </el-tooltip>
              <!-- 文件名 -->
              <span style="margin-left: 13px; font-size: 14px;">文件名</span>
              <!-- 收藏按钮 -->
              <el-tooltip class="item" effect="dark" content="收藏" placement="bottom">
                <el-button size="big" icon="	fa fa-bookmark-o" style="border: none; margin-left: 13px;"></el-button>
              </el-tooltip>
              <span style="margin-left: 13px; color:#a5a5a5; font-size: 14px;">文档将自动保存</span>
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
          <editor v-model="content"></editor>
        </el-main>
      </el-container>
    </el-container>
  </div>
  <!-- <div>
    <editor v-model="content" ></editor>
  </div>-->
</template>

<script>
import editor from "./EditorComponent";
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
  },
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
  margin-bottom: 5px;
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
  background-color: #f7f7f7;
  // background-color: #ffffff;
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
  // border: 1px solid red;
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
  display: flex;
  align-items: center;
  // margin: 2.5px 0;
  // background-color: #f9fafc;
}
</style>
