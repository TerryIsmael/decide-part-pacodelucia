<template>
    <div>
        <canvas ref="myChart" style="width: 100%; height: 400px;"></canvas>
    </div>
</template>

<script>
import Chart from 'chart.js/auto';
import axios from 'axios';

export default {
    data() {
        return {
            labels: [],
            data: [],
            colors: generateGreenScale(8), // Cambia el número según el nº de votaciones
        };
    },
    mounted() {
        this.fetchData();
    },
    methods: {
        fetchData() {
            axios.get('http://localhost:8000/voting/')
                .then(response => {
                    this.processData(response.data);
                    this.createChart();
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        },
        processData(data) {
            this.labels = data.map((voting, index) => `${voting.name}: ${voting.votes || 0} votes`);
            this.data = data.map(voting => voting.votes || 0);
        },

        createChart() {
            const ctx = this.$refs.myChart.getContext('2d');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: this.labels,
                    datasets: [{
                        label: 'Total Votes',
                        data: this.data,
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
    },
};

function generateGreenScale(numColors) {
    const colors = [];
    for (let i = 1; i < numColors; i++) {
        const greenValue = Math.round((255 / numColors) * i);
        const color = `rgba(1, ${greenValue}, 1, 255)`;
        colors.push(color);
    }
    return colors;
}
</script>

<style scoped>
/* Agrega estilos específicos del componente si es necesario */
</style>
