import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
import ListVoting from './components/ListVoting.vue';
import GraficaView from './components/GraficaView.vue';


const routes = [
  { path: '/admin/voting', component: ListVoting },
  { path: '/admin/grafica', component: GraficaView },
  { path: '/', component: HelloWorld }

];

const router = createRouter({
    routes,
    history: createWebHistory()
});

export default router;