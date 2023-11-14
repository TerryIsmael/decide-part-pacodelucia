import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Booth from './components/Booth.vue';
import UserLogin from './components/UserLogin.vue';
import Stats from './components/Stats.vue'

const routes = [
  { path: '/booth/:id', component: Booth },
  { path: '/login', component: UserLogin },
  { path: '/:id/stats', component: Stats },
  { path: '/', component: HelloWorld }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;