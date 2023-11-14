<template>
    <div>
      <h1>Estadisticas de la votación</h1>
      <h2>{{ stats.question }}</h2>
      <p>Total de votos: {{stats.votes}}</p>
      <p>Porcentaje de censo que ha votado: {{ stats.census }}%</p>
      <!-- Mostrar otras estadísticas según sea necesario -->
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  export default {
    data() {
      return {
        stats: {},
      };
    },
    mounted() {
      this.actualizarEstadisticas();
      setInterval(this.actualizarEstadisticas, 1000);
    },
  
    methods: {
        actualizarEstadisticas() {
        const votingId = this.$route.params.id;
        console.log(`Solicitando datos para la votación con id: ${votingId}`);

        axios.get(`http://localhost:8080/${votingId}/stats`)
            .then(response => {
            console.log('Datos recibidos:', response.data);
            this.stats = response.data;
            })
            .catch(error => {
            console.error('Error al obtener las estadísticas:', error);
            });
        },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos específicos del componente si es necesario */
  </style>