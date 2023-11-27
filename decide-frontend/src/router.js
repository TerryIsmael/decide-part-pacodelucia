import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Voting from './components/Voting.vue';
import Tokens from './components/Tokens.vue';
import Vote from './components/Vote.vue';
import Question from './components/Question.vue';

const routes = [
  { path: '/admin/voting', component: Voting },
  { path: '/admin/authtoken', component: Tokens },
  { path: '/admin/vote', component: Vote },
  { path: '/admin/question', component: Question },
  { path: '/', component: HelloWorld }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;

