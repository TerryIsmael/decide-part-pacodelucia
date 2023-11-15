import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Tokens from './components/Tokens.vue';
import AdminLogin from './components/AdminLogin.vue';

const routes = [
  { path: '/admin/authtoken', component: Tokens },
  { path: '/', component: HelloWorld },
  { path: '/admin/login', component: AdminLogin },
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;