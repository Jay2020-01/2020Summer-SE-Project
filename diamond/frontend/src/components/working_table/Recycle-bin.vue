<template>
  <div class="tabs_container">
    <!-- 标签组件 -->
    <el-tabs
      v-model="activeName"
      @tab-click="handleClick"
    >
      <!-- 标签内容 -->
      <el-tab-pane
        label="回收站"
        name="first"
      >
        <!-- 清空回收站是否确认的显示 -->
        <h6>这里是为了显示清空回收站按钮选择的哪一个，并方便以绑定事件,之后请删除</h6>
        <h5>点击了"{{ qingkong }}"</h5>
        <!-- 清空回收站图标与弹出框 -->
        <div style="text-align:right">
          <el-popconfirm
            confirm-button-text="好的"
            cancel-button-text="不用了"
            icon="el-icon-info"
            icon-color="red"
            title="确定删除所有文件吗？"
            @onConfirm="confirm"
          >
            <el-button
              slot="reference"
              title="清空回收站"
            >
              <i class="el-icon-delete" />
            </el-button>
          </el-popconfirm>
          <!-- <el-button type="primary" title="清空回收站" icon="el-icon-delete"></el-button> -->
        </div>
        <!-- 一行两个 -->
        <el-row :gutter="12">
          <el-col
            v-for="(o) in 5"
            :key="o"
            :span="8"
          >
            <!-- 文件卡片 -->
            <el-card shadow="hover">
              <div class="card-container">
                <!-- 图标 -->
                <div class="picture inline-div">
                  <span
                    class="fa fa-file-text-o"
                    style="font-size:25px"
                  />
                </div>
                <!-- 文字 -->
                <div class="word inline-div">
                  <div class="tile">
                    钻石文档
                  </div>
                  <div class="details">
                    今天 10:20 我 打开
                  </div>
                </div>

                <el-dropdown>
                  <!-- 后面的操作图标 -->
                  <span class="el-dropdown-link">
                    <i class="el-icon-arrow-down el-icon--right" />
                    <!-- 下拉图标 -->
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <!-- 选项 -->
                    <el-dropdown-item><i class="el-icon-refresh-left" />恢复文件</el-dropdown-item>
                    <el-dropdown-item><i class="el-icon-delete" />彻底删除</el-dropdown-item>
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
  data () {
    return {
      activeName: 'first',
      qingkong: '还没点'
    }
  },
  methods: {
    handleClick (tab, event) {
      console.log(tab, event)
    },
    confirm () {
      this.qingkong = '确定'
    }
  }
}
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
