import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import WorkingTable from '../components/working_table/WorkingTable.vue'
import MyInfo from '../components/myinfo/MyInfo.vue'
import Inbox from '../components/working_table/In-box.vue'
import Mydesktop from '../components/working_table/My-desktop.vue'

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
      {path: '/myinfo', component: MyInfo},
      {path: '/2', component: Inbox},
      {path: '/3', component: Mydesktop}
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router
