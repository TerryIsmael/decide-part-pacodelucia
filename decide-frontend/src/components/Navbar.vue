<template>
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
          <button class="logout-btn" v-if="logged" @click="logout()">Cerrar sesión</button>
          <button class="login-btn" v-else @click="$router.push('/login')">Iniciar sesión</button>
        </div>
      </div>
    </nav>
</template>
  
<script>
    export default {
        name: 'Navbar',
        props: ['logged', 'username'],
        methods: {
            logout() {
                document.cookie = 'decide=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                this.$router.push('/').then(() => { this.$router.go(0); });
            },
        },
    };
</script>

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
    border: 1px solid white;
    border-radius: 5px;
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
    border: 1px solid white;
    border-radius: 5px;
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