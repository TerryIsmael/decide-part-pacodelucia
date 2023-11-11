import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import ListVoting from './components/ListVoting.vue';

const routes = [
  { path: '/admin/voting', component: ListVoting },
  { path: '/', component: HelloWorld }
];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;