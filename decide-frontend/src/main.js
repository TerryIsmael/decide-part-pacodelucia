import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import navbarAdmin from './components/NavbarAdmin.vue';
import './style.css'

const app = createApp(App);
app.use(router);
app.component('navbarAdmin', navbarAdmin);

app.mount('#app');