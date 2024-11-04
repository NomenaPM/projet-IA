import { createRouter, createWebHistory } from 'vue-router'
import Affichage from '@/views/Affichage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'affichage',
component:Affichage
    },
  
  ]
})

export default router
