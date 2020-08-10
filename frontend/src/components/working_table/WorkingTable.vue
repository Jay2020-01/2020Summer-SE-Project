<template>
  <div class="tabs_container">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="最近浏览" name="first">
        <el-row>
          <el-col :span="8" v-for="(o, index) in 2" :key="o" :offset="index > 0 ? 2 : 0">
            <el-card :body-style="{ padding: '0px' }">
              <img
                src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png"
                class="image"
              />
              <div style="padding: 14px;">
                <span>好吃的汉堡</span>
                <div class="bottom clearfix">
                  <time class="time">{{ currentDate }}</time>
                  <el-button type="text" class="button">操作按钮</el-button>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-tab-pane>
      <el-tab-pane label="我创建的" name="second">配置管理</el-tab-pane>
      <el-tab-pane label="我的收藏" name="third">角色管理</el-tab-pane>
      <el-tab-pane label="团队文档" name="fourth">定时任务补偿</el-tab-pane>
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
.tabs_container {
  // border: 1px solid red;
}
.tabs_container /deep/.el-tabs__nav-wrap::after {
  position: static !important;
}
</style>