import { createApp, ref } from 'vue';
import App from './App.vue';
import navbarAdmin from './components/NavbarAdmin.vue';
import router from './router.js';
import './style.css'

const app = createApp(App);
app.use(router);
app.component('navbarAdmin', navbarAdmin);

app.provide('logged', ref(false));
app.provide('username', ref(''));
app.provide('navBarLoaded', ref(false));

app.mount('#app');