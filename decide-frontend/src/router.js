import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Booth from './components/Booth.vue';
import UserLogin from './components/UserLogin.vue';
import PageNotFound from './components/PageNotFound.vue';

const routes = [
  { path: '/booth/:id', component: Booth },
  { path: '/login', component: UserLogin },
  { path: '/', component: HelloWorld },
  { path: '/:pathMatch(.*)*', component: PageNotFound  }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;