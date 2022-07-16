import Vue from 'vue'
import VueRouter from 'vue-router'
import MainPage from '../components/MainPage.vue'
import FicheMeta from '../components/FicheMeta.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: MainPage
  },
  {
    path: ':id',
    name: 'fiche',
    component: FicheMeta
  }
]

const router = new VueRouter({
  routes
})

export default router
