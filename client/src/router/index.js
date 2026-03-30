import { createRouter, createWebHistory } from 'vue-router'
import Add_View from '../views/Add_View.vue'
import Edit_View from '../views/Edit_View.vue'
import Testing_View from '../views/Testing_View.vue'

const routes = [
  { path: '/', name: 'Testing', component: Testing_View },
  { path: '/add', name: 'Add', component: Add_View },
  { path: '/edit', name: 'Edit', component: Edit_View },        // list view
  { path: '/edit/:id', name: 'EditProfile', component: Edit_View } // detail view
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router