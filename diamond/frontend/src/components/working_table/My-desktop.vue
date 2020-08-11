<template>
  <div class="tabs_container">
    <!-- 标签组件 -->
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <!-- 标签内容 -->
      <el-tab-pane label="我的桌面" name="first">
            <!-- 下面这个是选择“平铺”还是“列表”的两个按钮 -->
            <div style="text-align:right">
                <i class="el-icon-menu" value="平铺" @click="topingpu"></i>
                <i class="el-icon-s-operation" value="列表" @click="toliebiao"></i>
            </div>

        <!-- 如果是平铺就是下面这些 -->
        <!-- 一行两个 -->
        <el-row :gutter="12" v-if="pingpu">
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

        <!-- 如果是选择列表就展示下面这些 -->
        <el-table
            :data="tableData"
            height="520"
            border
            style="width: 100%"
            v-if="liebiao">
            <el-table-column
                prop="name"
                label="文件名"
                width="900">
            </el-table-column>
            <el-table-column
                prop="author"
                label="创建者"
                width="180">
            </el-table-column>
            <el-table-column
                prop="lasttime"
                label="更新时间">
            </el-table-column>
        </el-table>

        </el-tab-pane>
        </el-tabs>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeName: "first",
      pingpu:true,
      liebiao:false,
      tableData: [{
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }, {
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }, {
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }, {
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }, {
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }, {
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }, {
          name:'一分钟，了解金刚石文档',
          author:'921049836',
          lasttime:'今天23：29'
        }]
    };
  },
  methods: {
    handleClick(tab, event) {
      console.log(tab, event);
    },
    topingpu:function(){
        this.pingpu=true;
        this.liebiao=false;
    },
    toliebiao:function(){
        this.pingpu=false;
        this.liebiao=true;
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
.el-icon-menu{
    cursor:pointer;
}
.el-icon-menu:hover{
    transform:scale(1.3);
}
.el-icon-s-operation{
    cursor:pointer;
}
.el-icon-s-operation:hover{
    transform:scale(1.3);
}
</style>