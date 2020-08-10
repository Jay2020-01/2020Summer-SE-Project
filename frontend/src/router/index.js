import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import WorkingTable from '../components/working_table/WorkingTable.vue'
import MyInfo from '../components/myinfo/MyInfo.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/myinfo' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  {
    path: '/home',
    component: Home,
    children: [
      {path: '/1', component: WorkingTable},
      {path: '/myinfo', component: MyInfo}
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
