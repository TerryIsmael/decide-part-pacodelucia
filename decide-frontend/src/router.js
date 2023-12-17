import { createRouter, createWebHistory } from 'vue-router';
import Voting from './components/Voting.vue';
import Tokens from './components/Tokens.vue';
import AdminLogin from './components/AdminLogin.vue';
import Vote from './components/Vote.vue';
import Question from './components/Question.vue';
import AdminHome from './components/AdminHome.vue';
import Mixnet from './components/Mixnet.vue';
import User from './components/User.vue';
import Auth from './components/Auth.vue';
import Census from './components/Census.vue';
import Home from './components/Home.vue';
import Booth from './components/Booth.vue';
import UserLogin from './components/UserLogin.vue';
import Stats from './components/Stats.vue';
import Register from './components/Register.vue';
import EmailAuthentication from './components/EmailAuthentication.vue';
import PageNotFound from './components/PageNotFound.vue';
import UserData from './components/UserData.vue';
import Grafica from './components/GraficaView.vue';

const routes = [
  { path: '/admin/voting', component: Voting },
  { path: '/admin/authtoken', component: Tokens },
  { path: '/', component: Home },
  { path: '/admin/login', component: AdminLogin },
  { path: '/admin/vote', component: Vote },
  { path: '/admin/question', component: Question },
  { path: '/admin/mixnet', component: Mixnet },
  { path: '/admin/user', component: User },
  { path: '/admin/userdata', component: UserData },
  { path: '/admin/auth', component: Auth },
  { path: '/admin/census', component: Census },
  { path: '/admin', component: AdminHome},
  { path: '/register', component: Register },
  { path: '/authEmail', component: EmailAuthentication },
  { path: '/booth/:id', component: Booth },
  { path: '/login', component: UserLogin },
  { path: '/:id/stats', component: Stats },
  { path: '/:pathMatch(.*)*', component: PageNotFound },
  { path: '/admin/grafica', component: Grafica },
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;
