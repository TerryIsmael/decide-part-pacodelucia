import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Register from './components/Register.vue'

const routes = [
  { path: '/', component: HelloWorld },
  { path: '/register', component: Register }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;