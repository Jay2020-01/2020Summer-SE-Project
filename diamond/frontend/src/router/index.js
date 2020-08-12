import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Login.vue'
import Home from '../components/Home.vue'
import Register from '../components/Register.vue'
import WorkingTable from '../components/working_table/WorkingTable.vue'
import MyInfo from '../components/myinfo/MyInfo.vue'
import Inbox from '../components/working_table/In-box.vue'
import Mydesktop from '../components/working_table/My-desktop.vue'
import Editor from '../components/editor/Editor.vue'
import Test from '../components/editor/Test.vue'
import Recyclebin from '../components/working_table/Recycle-bin.vue'
import Team1 from '../components/working_table/team1.vue'
import Team2 from '../components/working_table/team2.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/Editor' },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/editor', component: Editor},
  {
    path: '/home',
    component: Home,
    children: [
      {path: '/1', component: WorkingTable},
      {path: '/myinfo', component: MyInfo},
      {path: '/2', component: Inbox},
      {path: '/3', component: Mydesktop},
      {path: '/4-1', component: Team1},
      {path: '/4-2', component: Team2},
      {path: '/5', component: Recyclebin}
    ]
  }
]

const router = new VueRouter({
  routes
})

export default router