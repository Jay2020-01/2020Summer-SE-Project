<template>
  <div class="tabs_container">
    <!-- 标签组件 -->
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <!-- 标签内容 -->
      <el-tab-pane label="收件箱" name="first">
        <!-- 一行两个 -->
        <el-row :gutter="12">
          <el-col v-for="(o) in 2" :key="o" :span="8">
            <!-- 文件卡片 -->
            <el-card shadow="hover">
              <div class="card-container">
                <!-- 图标 -->
                <div class="picture inline-div">
                  <span class="fa fa-file-text-o" style="font-size:25px"></span>
                </div>
                <!-- 文字 -->
                <div class="word inline-div">
                  <div class="tile">钻石文档</div>
                  <div class="details">今天 10:20 我 打开</div>
                </div>
                
                <el-dropdown>
                <!-- 后面的操作图标 -->
                  <span class="el-dropdown-link">
                    <i class="el-icon-arrow-down el-icon--right"></i>
                    <!-- 下拉图标 -->
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <!-- 选项 -->
                    <el-dropdown-item><i class="el-icon-magic-stick"></i>新标签页打开</el-dropdown-item>
                    <el-dropdown-item><i class="el-icon-delete"></i>删除</el-dropdown-item>
                    <el-dropdown-item>其他操作请补充</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>

    </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: "first",
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
  },
};
</script>

<style lang="less" scoped>
// 切换标签样式
// 取消下方横线
.tabs_container /deep/.el-tabs__nav-wrap::after {
  position: static !important;
}

// 卡片样式
.el-card {
  margin: 20px;
}
// 卡片内容样式
.card-container {
  align-items: center;
  display: flex;
}
.inline-div {
  display: inline-block;
}
.picture {
  box-sizing: border-box;
  align-items: center;
  width: 25%;
}
.word {
  width: 70%;
  text-align: left;
}
.title {
  font-size: 14px;
}
.details {
  margin-top: 3px;
  font-size: 11px;
  color: #999;
}
.el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
  }
  .el-icon-arrow-down {
    font-size: 12px;
  }
</style>