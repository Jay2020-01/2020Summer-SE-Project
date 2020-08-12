<template>
  <div class="myinfo_container">
    <el-card class="box-card" shadow="hover">
      <div slot="header" class="clearfix">
        <span>账号信息</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="confirm_modify">确认修改</el-button>
      </div>
      <div class="text item">
        <el-form :model="registerForm" class="register_form" label-width="0px">
          <!-- 用户名 -->
          <el-form-item label>
            <el-input v-model="registerForm.username" prefix-icon="fa fa-user" placeholder="用户名"></el-input>
          </el-form-item>
          <!-- 密码 -->
          <el-form-item label>
            <el-input
              v-model="registerForm.password"
              show-password
              prefix-icon="fa fa-lock"
              placeholder="密码"
            ></el-input>
          </el-form-item>
          <!-- 手机号 -->
          <el-form-item label>
            <el-input
              v-model="registerForm.phone_number"
              prefix-icon="fa fa-phone-square"
              placeholder="手机"
            ></el-input>
          </el-form-item>
          <!-- 邮箱 -->
          <el-form-item label>
            <el-input
              v-model="registerForm.mail_address"
              prefix-icon="fa fa-envelope"
              placeholder="邮箱"
            ></el-input>
          </el-form-item>
          <!-- 微信号 -->
          <el-form-item label>
            <el-input v-model="registerForm.wechat" prefix-icon="fa fa-wechat" placeholder="微信"></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    data() {
      return {
        // 注册表单的数据绑定对象
        registerForm: {
          username: "Tom",
          password: "12345",
          confirm_password: "",
          phone_number: "400-123-345",
          mail_address: "letmesee@gmail.com",
          wechat: "abaaba123",
        },
      };
    },
    methods: {
      tologin() {
        this.$router.push("/login");
      },
      confirm_modify() {
        axios.post('api/address/new', this.registerForm)
          .then((res) => {
            this.$router.push("/login")
          })
      }
    },
  };
</script>

<style lang="less" scoped>
  .myinfo_container {
    // 设置背景图片
    background-image: url("../../assets/backgroud-main.png");
    background-repeat: no-repeat;
    background-size: 100% 100%;
    -moz-background-size: 100% 100%;
    background-color: #2b4b6b;
    height: 100%;

  }

  .register_form {
    bottom: 5px;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }

  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {

    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both;
  }

  .box-card {
    width: 400px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-40%, -50%);
  }
</style>
