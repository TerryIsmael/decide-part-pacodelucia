<script>
import { ref, onMounted, inject } from "vue";

export default {
  setup() {
    const isInAdmin = inject("isInAdmin");
    const logged = inject("loggedUser");
    const username = inject("userUsername");
    const token = ref(null);
    const error = inject("userError");

    const logout = () => {
      document.cookie = 'decide=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      logged.value = false;
      window.location.href = '/';
    }

    const isLogged = () => {
      if (!isInAdmin.value) {
        var cookies = document.cookie.split(';');
        cookies.forEach((cookie) => {
          var pair = cookie.split('=');
          if (pair[0].trim() === 'decide' && pair[1]) {
            token.value = pair[1];
          } else {
            return logged.value = false;
          }
        });
      }
      fetch(import.meta.env.VITE_API_URL + '/gateway/authentication/getuser/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          token: token.value,
        }),
      })
        .then((response) => {
          if (response.ok) {
            logged.value = true;
            return response.json();
            
          } else {
            throw new Error('Error obteniendo el usuario');
          }
        })
        .then((data) => {
          logged.value = true;
          username.value = data.username;
          return response.json();
        })
        .catch((error) => {
          error.value = error.message
        });
    }

    onMounted(isLogged);

    return {
      error,
      logged,
      username,
      isInAdmin,
      isLogged,
      logout,
    }
  }
}
</script>

<template>
  <div v-if="!isInAdmin">
    <nav class="navbar">
      <div class="navbar-left">
        <a href="/">
          <h3 class="decide">Decide</h3>
        </a>
      </div>
      <div class="navbar-right">
        <div v-if="logged && username" class="usuario">
          <p>Usuario: </p>
          <p class="username" v-if="logged && username">{{ username }}</p>
        </div>
        <div class="buttons">
          <button class="logout-btn" style="margin: 0%;" v-if="logged" @click="logout()">Cerrar sesión</button>
          <button class="login-btn" style="margin: 0%" v-else @click="$router.push('/login')">Iniciar sesión</button>
        </div>
      </div>
    </nav>
  </div>
</template>

<style scoped>
.navbar {
  background-color: lightslategrey;
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
}

.login-btn {
  background-color: #045b96;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  color: white;
  font-size: 18px;
  cursor: pointer;
}

.login-btn:hover {
  background-color: #3490db;
}

.logout-btn {
  background-color: #c73525;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  color: white;
  font-size: 18px;
  cursor: pointer;
}

.logout-btn:hover {
  background-color: #d64434;
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