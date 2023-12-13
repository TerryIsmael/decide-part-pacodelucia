import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Booth from './components/Booth.vue';
import UserLogin from './components/UserLogin.vue';
import Stats from './components/Stats.vue'
import Register from './components/Register.vue'
import EmailAuthentication from './components/EmailAuthentication.vue'
import ListVoting from './components/ListVoting.vue';
import GraficaView from './components/GraficaView.vue';
import VotingStats from './components/VotingStats.vue';


const routes = [
  { path: '/booth/:id', component: Booth },
  { path: '/login', component: UserLogin },
  { path: '/:id/stats', component: Stats },
  { path: '/', component: HelloWorld },
  { path: '/register', component: Register },
  { path: '/authEmail', component: EmailAuthentication },
  { path: '/admin/voting', component: ListVoting },

  { path: '/admin/grafica', component: GraficaView },
  { path: '/', component: HelloWorld }
  { path: '/admin/voting/stats', component: VotingStats },
 ];




const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;