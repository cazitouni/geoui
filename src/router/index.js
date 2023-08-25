import Vue from 'vue'
import VueRouter from 'vue-router'
import MainPage from '../components/MainPage.vue'
import FicheMeta from '../components/FicheMeta.vue'
import CatalogSig from '../components/CatalogSig.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'main',
    component: MainPage
  },
  {
    path: '/catalog',
    name: 'catalog',
    component: CatalogSig
  },
  {
    path: '/:id',
    name: 'fiche',
    component: FicheMeta
  }
]

const router = new VueRouter({
  routes
})

export default router
