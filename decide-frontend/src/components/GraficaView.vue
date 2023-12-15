<template>
    <div>
      <div>
        <button v-for="(voting, index) in votings" :key="index" @click="showDetails(voting)">
          {{ voting.name }}
        </button>
      </div>
      <div>
        <canvas ref="myChart" style="width: 100%; height: 400px;"></canvas>
      </div>
      <div v-if="selectedVoting">
        <h2>{{ selectedVoting.name }} Details</h2>
        <ul>
          <li v-for="(tally, questionIndex) in selectedVoting.tally" :key="questionIndex">
            {{ getOptionName(questionIndex) }}: {{ [tally].length || 0 }} votes
          </li>
        </ul>
        <!-- Nueva sección para la gráfica de detalles -->
        <div>
            <canvas ref="detailChartCanvas" style="width: 50%; height: 300px;"></canvas>        
        </div>
      </div>
    </div>
  </template>
 <script>
 import Chart from 'chart.js/auto';
 import axios from 'axios';
 
 export default {
   data() {
     return {
       votings: [],
       selectedVoting: null,
       colors: generateRandomColors(10),
       detailChart: null,
     };
   },
   mounted() {
     this.fetchData();
   },
   methods: {

    getOptionName(optionIndex) {
    return this.selectedVoting.question.options[optionIndex];
    },

     fetchData() {
       axios.get('http://localhost:8000/voting/')
         .then(response => {
           this.votings = response.data;
           this.createChart();
         })
         .catch(error => {
           console.error('Error fetching data:', error);
         });
     },
     createChart() {
       const ctx = this.$refs.myChart.getContext('2d');
       new Chart(ctx, {
         type: 'bar',
         data: {
           labels: this.votings.map(voting => voting.name),
           datasets: [{
             label: 'Total Votes',
             data: this.votings.map(voting => voting.tally.length || 0),
             backgroundColor: this.colors,
             borderWidth: 1,
           }],
         },
         options: {
           scales: {
             y: {
               beginAtZero: true,
             },
           },
         },
       });
     },
     createDetailChart() {
       this.$nextTick(() => {
         if (this.detailChart) {
           this.detailChart.destroy();
         }
         const detailCtx = this.$refs.detailChartCanvas.getContext('2d');
         this.detailChart = new Chart(detailCtx, {
           type: 'pie',
           data: {
             labels: [],
             datasets: [{
               label: 'Votos',
               data: this.selectedVoting.tally.map(optionTally => [optionTally].length || 0),
               backgroundColor: this.colors,
               borderWidth: 1,
             }],
           },
           options: {
             scales: {
               y: {
                 beginAtZero: true,
               },
             },
           },
         });
       });
     },
     showDetails(voting) {
       this.selectedVoting = voting;
       this.createDetailChart();
     },
   },
 };
 
 // Función para generar la escala de colores
 function generateRandomColors(numColors) {
  const colors = [];
  for (let i = 0; i < numColors; i++) {
    const randomColor = getRandomColor();
    colors.push(randomColor);
  }
  return colors;
}

function getRandomColor() {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

 </script>
 
 <style scoped>
 /* Agrega estilos específicos del componente si es necesario */
 </style>