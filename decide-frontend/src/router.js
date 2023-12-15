import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
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

const routes = [
  { path: '/admin/voting', component: Voting },
  { path: '/admin/authtoken', component: Tokens },
  { path: '/', component: HelloWorld },
  { path: '/admin/login', component: AdminLogin },
  { path: '/admin/vote', component: Vote },
  { path: '/admin/question', component: Question },
  { path: '/admin/mixnet', component: Mixnet },
  { path: '/admin/user', component: User },
  { path: '/admin/auth', component: Auth },
  { path: '/admin/census', component: Census },
  { path: '/admin', component: AdminHome}
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;

