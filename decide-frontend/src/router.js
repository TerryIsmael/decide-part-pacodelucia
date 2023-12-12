import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import Booth from './components/Booth.vue';
import UserLogin from './components/UserLogin.vue';
import PageNotFound from './components/PageNotFound.vue';

const routes = [
  { path: '/booth/:id', component: Booth },
  { path: '/login', component: UserLogin },
  { path: '/', component: Home },
  { path: '/:pathMatch(.*)*', component: PageNotFound  }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;