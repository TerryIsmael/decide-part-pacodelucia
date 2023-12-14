import { createRouter, createWebHistory } from 'vue-router';
import Register from './components/Register.vue'
import EmailAuthentication from './components/EmailAuthentication.vue'
import Booth from './components/Booth.vue'
import UserLogin from './components/UserLogin.vue'
import Home from './components/Home.vue'
import PageNotFound from './components/PageNotFound.vue'


const routes = [
  { path: '/', component: Home },
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