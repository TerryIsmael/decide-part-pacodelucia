import { createApp, ref } from 'vue';
import App from './App.vue';
import navbarAdmin from './components/NavbarAdmin.vue';
import navbar from './components/Navbar.vue';
import router from './router.js';
import './style.css'

const app = createApp(App);
app.use(router);
app.component("navbarAdmin", navbarAdmin);
app.component("navbarUser", navbar);

app.provide("logged", ref(false));
app.provide("username", ref(''));
app.provide("navBarLoaded", ref(false));
app.provide("isInAdmin", ref(false));
app.provide("loggedUser", ref(false));
app.provide("userUsername", ref(''));
app.provide("userError", ref(''));
app.provide("inLogin", ref(false));

app.mount('#app');