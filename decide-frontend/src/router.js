import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Register from './components/Register.vue'
import EmailAuthentication from './components/EmailAuthentication.vue'

const routes = [
  { path: '/', component: HelloWorld },
  { path: '/register', component: Register },
  { path: '/authEmail', component: EmailAuthentication },
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