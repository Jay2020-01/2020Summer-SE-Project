import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Axios from 'axios'
import './plugins/element.js'
// 导入全局样式表
import './assets/css/global.css'
// 引入font-awesome
import 'font-awesome/css/font-awesome.css'

Vue.prototype.$http = Axios
const token = localStorage.getItem('token')
if (token) {

}
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
