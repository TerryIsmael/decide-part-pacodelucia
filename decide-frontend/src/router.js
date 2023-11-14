import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import ListVoting from './components/ListVoting.vue';
import VotingStats from './components/VotingStats.vue';

const routes = [
  { path: '/admin/voting', component: ListVoting },
  { path: '/admin/voting/stats', component: VotingStats },
  { path: '/', component: HelloWorld }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;