<script>
import { ref, onMounted, inject } from "vue";
import { useRouter } from "vue-router";

export default {
  setup() {
    const router = useRouter();
    const logged = inject('logged')
    const username = inject('username')
    const error = ref(null)
    const navBarLoaded = inject('navBarLoaded')
    const isInAdmin = inject('isInAdmin')

    const isLogged = () => {
      if (!window.location.href.includes("/admin")) {
        return isInAdmin.value = false
      }
      isInAdmin.value = true
      fetch(import.meta.env.VITE_API_URL + '/authentication/admin-auth/', {
        method: 'GET',
        credentials: 'include',
      })
        .then((response) => {
          if (response.ok) {
            navBarLoaded.value = true;
            logged.value = true;
            return response.json();
          } else {
            if (window.location.href != window.location.origin + "/admin/login") {
              window.location.href = window.location.origin + "/admin/login"
            }
          }
        })
        .then((data) => {
          if (data.user_data.is_staff) {
            logged.value = true;
            username.value = data.user_data.username
          } else {
            if (window.location.href != window.location.origin + "/admin/login") {
              window.location.href = window.location.origin + "/admin/login"
            }
          }
        })
        .catch(() => {
          if (window.location.href != window.location.origin + "/admin/login") {
            window.location.href = window.location.origin + "/admin/login"
          }
        });
    }

    const logout = () => {
      document.cookie = 'sessionid=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      fetch(import.meta.env.VITE_API_URL + '/admin/logout/', {
        method: 'GET',
        credentials: 'include',
      })
        .then((response) => {
          if (response.ok) {
            logged.value = false;
            window.location.href = "/admin/login"
          } else {
            form = true;
          }
        })
    };

    onMounted(isLogged);

    return {
      logged,
      username,
      error,
      router,
      isInAdmin,
      isLogged,
      logout,
    }
  }
}
</script>

<template>
  <div v-if="isInAdmin">
    <nav class="navbar">
      <div class="navbar-left">
        <a href="/admin">
          <h3 class="decide">Decide Admin</h3>
        </a>
      </div>
      <div class="navbar-right">
        <div v-if="logged && username" class="usuario">
          <p>Usuario: </p>
          <p class="username" v-if="logged && username">{{ username }}</p>
        </div>

        <div class="buttons">
          <button class="logout-btn" v-if="logged" @click="logout()">Cerrar sesión</button>
          <button class="login-btn" v-else @click="router.push('/admin/login')">Iniciar sesión</button>
        </div>

      </div>
    </nav>
  </div>
</template>
  
<style scoped>
.navbar {
  width: auto;
  background-color: rgb(0, 139, 139);
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.nav-list {
  list-style: none;
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 100%;
}

.nav-list li {
  margin: 0 10px;
}

.nav-list li a {
  color: white;
  text-decoration: none;
  font-size: 18px;
}

.buttons {
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-btn {
  background-color: rgb(0, 48, 48);
  font-size: 18px;
  cursor: pointer;
  margin-bottom: 0;
}

.login-btn:hover {
  background-color: rgb(117, 205, 205);
  color: black;
}

.logout-btn {
  background-color: rgb(211, 91, 91);
  color: white;
  font-size: 18px;
  cursor: pointer;
  margin-bottom: 0;
}

.logout-btn:hover {
  background-color: rgb(211, 91, 91);
}

.decide {
  font-family: 'Roboto', sans-serif;
  font-size: 26px;
  font-weight: bold;
  color: #ffffff;
  letter-spacing: 2px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.username {
  font-family: 'Roboto', sans-serif;
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
  margin-right: 20px;
  margin-left: 10px;
}

.usuario {
  display: flex;
  align-items: center;
}
</style>