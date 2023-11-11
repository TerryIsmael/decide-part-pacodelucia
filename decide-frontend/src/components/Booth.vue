<template>
    <div v-if="voting">
        <h1>{{ voting.name }}</h1>
        <p>{{ voting.desc }}</p>
        <p>Question: {{ voting.question.desc }}</p>
        <ul>
            <li v-for="option in voting.question.options" :key="option.number">
                <input type="radio" :id="option.number" :value="option.number" v-model="selectedOption">
                <label :for="option.id">{{ option.option }}</label>
            </li>
        </ul>
        <button @click="vote">Vote</button>
    </div>
    <div v-else>
        Cargando...
    </div>
</template>

<script>
export default {
    name: 'Booth',
    data() {
        return {
            voting: null,
            selectedOption: null,
        };
    },
    created() {
        fetch(import.meta.env.VITE_API_URL + '/voting/?id=' + this.$route.params.id)
            .then((response) => response.json())
            .then((data) => {
                this.voting = data[0];
            });
    },
    methods: {
        vote() {
            console.log(this.selectedOption);
        }
    },
};
</script>

<style scoped>
/* Tus estilos van aquí */
</style>