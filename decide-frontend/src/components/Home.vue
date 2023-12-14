<template>
  <Navbar :logged="userLogged" :username="user?.username"/>
  <p class="error" v-if="error"> {{ error }}</p>
  <p class="voting-p" v-if="userLogged">Votaciones abiertas</p>
  <div class="voting-container" v-if="dataLoaded && userLogged">
    <div class="voting-card" v-for="voting in openVotings" :key="voting.id">
        <div class="voting-title">
            {{ voting.name }}
        </div>
        <div class="voting-body">
          <div>
            <p class="descripcion">{{ voting.desc }} </p>
          </div>
          <p class="fecha">Inicio: {{ formatDate(voting.start_date) }} </p>
          <button class="btn" @click="$router.push('/booth/' + voting.id)">Votar</button>
        </div>
        
      </div>
  </div>
  <p class="voting-p" v-if="userLogged">Votaciones próximas</p>
  <div class="voting-container" v-if="dataLoaded && userLogged">
    <div class="voting-card" v-for="voting in futureVotings" :key="voting.id">
        <div class="voting-title">
            {{ voting.name }}
        </div>
        <div class="voting-body">
          <div>
            <p class="descripcion">{{ voting.desc }} </p>
          </div>
          <button class="btn" :disabled="true">Votar</button>
        </div>
        
      </div>
  </div>
  <p class="voting-p" v-if="userLogged">Votaciones finalizadas</p>
  <div class="voting-container" v-if="dataLoaded && userLogged">
    <div class="voting-card" v-for="voting in finishedVotings" :key="voting.id">
        <div class="voting-title">
            {{ voting.name }}
        </div>
        <div class="voting-body">
          <div>
            <p class="descripcion">{{ voting.desc }} </p>
          </div>
          <p class="fecha">Inicio: {{ formatDate(voting.start_date) }} </p>
          <p class="fecha">Fin: {{ formatDate(voting.end_date) }} </p>
          <button class="btn" @click="$router.push('/visualizer/' + voting.id)">Resultados</button>
        </div>
        
      </div>
  </div>
  <p class="voting-p" v-if="!userLogged">Inicia sesión para ver tus votaciones</p>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'Home',
  components: {
    Navbar,
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      dataLoaded: false,
      userLogged: false,
      error: null,
      user: null,
      openVotings: [],
      futureVotings: [],
      finishedVotings: [],
    }
  }, 
  created() {
    this.init();
  },
  methods: {
    init() {
      var cookies = document.cookie.split(';');
      cookies.forEach((cookie) => {
          var pair = cookie.split('=');
          if (pair[0].trim() === 'decide' && pair[1]) {
              this.token = pair[1];
              this.isLogged();
          }
      });
    }, 
    isLogged() {
      fetch(import.meta.env.VITE_API_URL + 'gateway/authentication/getuser/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          token: this.token,
      }),
      })
      .then((response) => {
          if (response.ok) {
            console.log("response: ",response);
              return response.json();
          } else {
              throw new Error('Error obteniendo el usuario');
          }
      })
      .then((data) => {
          this.userLogged = true;
          this.user = data;
          this.getData();
      })
      .catch((error) => {
        this.error = error.message
      });
          
      },
      getData(){
    },
    getData() {
      fetch(import.meta.env.VITE_API_URL + 'voting/getbyuser', {
        method: 'GET',
        credentials: 'include',
      })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Error obteniendo las votaciones');
        }
      })
      .then((data) => {
        var votings = data.votings;
        this.openVotings = votings.filter((voting) => {
          return voting.start_date && !voting.end_date;
        });
        this.futureVotings = votings.filter((voting) => {
          return !voting.start_date;
        });
        this.finishedVotings = votings.filter((voting) => {
          return voting.start_date && voting.end_date;
        });
        this.dataLoaded = true;
      })
      .catch((error) => {
        this.error = error.message;
      });
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
      const date = new Date(dateString);
      return new Intl.DateTimeFormat('es-ES', options).format(date);
    }
  }
}
</script>

<style scoped>
  .error {
    color: red;
  }
  
  .voting-container {
  align-items: start;
	display: grid;
	grid-gap: 16px;
	grid-template-columns: auto auto auto;
	justify-content: center;
  }

.voting-card {
  background-color: rgb(255, 255, 255);
  width: 500px;
  height: 300px;
	border-radius: 5px;
	color: white;
  margin: 25px;
}

.voting-p {
  color: white;
  font-size: 30px;
  text-align: center;
  margin: 25px;
}

.voting-title {
  width: 100%;
  height: 50px;
  background-color: lightskyblue;
  font-size: 30px;
  font-weight: bold;
  text-align: center;
  color: black;
  border-radius: 5px;
}

.descripcion {
  margin-left: 30px;
  font-size: 20px;
  color: black;
  text-align: left;
}

.fecha {
  margin-left: 30px;
  font-size: 20px;
  text-align: left;
  color: black;
  font-weight: 1;
  margin-top: auto;
  height: 100%;
}

.voting-body {
  width: 500px;
  height: 230px;
  margin-top: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.btn {
  background-color: #045b96;
  border: 1px solid rgb(0, 0, 0);
  border-radius: 5px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 10px;
  width: 150px;
  align-self: center;
}

.btn:hover {
  background-color: #51a2e6;
}

.btn:disabled {
  background-color: #c7c7c7;
  cursor: not-allowed;
}

</style>
