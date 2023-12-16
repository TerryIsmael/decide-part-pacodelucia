import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import Booth from './components/Booth.vue';
import UserLogin from './components/UserLogin.vue';
import Stats from './components/Stats.vue'
import Register from './components/Register.vue'
import EmailAuthentication from './components/EmailAuthentication.vue'
import PageNotFound from './components/PageNotFound.vue';

import ListVoting from './components/ListVoting.vue';
import GraficaView from './components/GraficaView.vue';
import VotingStats from './components/VotingStats.vue';


const routes = [
  { path: '/', component: Home },
  { path: '/register', component: Register },
  { path: '/authEmail', component: EmailAuthentication },
  { path: '/booth/:id', component: Booth },
  { path: '/login', component: UserLogin },
  { path: '/:id/stats', component: Stats },
  { path: '/:pathMatch(.*)*', component: PageNotFound  }

  { path: '/admin/voting', component: ListVoting },

  { path: '/admin/grafica', component: GraficaView },
  { path: '/', component: HelloWorld },
  { path: '/admin/voting/stats', component: VotingStats },
];




const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;