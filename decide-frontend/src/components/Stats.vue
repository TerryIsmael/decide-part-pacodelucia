<template>
  <div>
    <h1>Estadisticas de la votación: {{ stats.question }}</h1>
    <table>
      <tr>
        <th>Total de votos</th>
        <th>Porcentaje de censo que ha votado</th>
        <th>Media del tiempo entre votos</th>
      </tr>
      <tr>
        <td>{{stats.votes}}</td>
        <td>{{ stats.census }}%</td>
        <td>{{stats.avg_time_diff}} min</td>
      </tr>
    </table>
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
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
  }
  </style>