import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/landing-page',
      name: 'landingPage',
      component: () => import('../views/LandingView.vue')
    },
    {
      path: '/audit',
      name: 'audit',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AuditView.vue')
    },
    {
      path: '/documents/:uid',
      name: 'document',
      component: () => import('../views/DocumentView.vue'),
      props: true,
    },
    {
      path: '/:catchAll(.*)',
      name: 'notFound',
      component: () => import('../views/LandingView.vue')
    }
  ]
})

export default router
