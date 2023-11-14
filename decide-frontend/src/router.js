import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import Voting from './components/Voting.vue';

const routes = [
  { path: '/admin/voting', component: Voting },
  { path: '/', component: HelloWorld }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;