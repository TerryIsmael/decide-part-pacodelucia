<template>
    <div v-if="successVote">
        <h1 style="color:lightgreen">¡Voto realizado con éxito!</h1>
        <h2>Usted ha votado: {{ selectedDescription }}</h2>
        <button @click="redirectToHomePage">Página Principal</button>
    </div>
    <div class="voting-container" v-if="voting && user && !errorMessage && !successVote">
        <h1 class="voting-name">{{ voting.name }}</h1>
        <p class="voting-desc">{{ voting.desc }}</p>
        <h2 class="question">{{ voting.question.desc }}</h2>
        <ul>
            <li v-for="option in voting.question.options" :key="option.number" 
                :class="{ 'selected': selectedOption === option.number }" 
                @click="selectedOption = option.number; selectedDescription = option.option">
            <label :for="option.id">{{ option.option }}</label>
    </li>
        </ul>
        <button class="vote-button" @click="vote">VOTAR</button>
    </div>
    <div class="error-screen" v-if="errorMessage">
        <div class="error-message">
            {{ errorMessage }}
        </div>
        <div v-if="goHomeButton">
            <button @click="redirectToHomePage">Página Principal</button>
        </div>
    </div>
    <div style="padding-top: 50%;" v-if="(!voting || !user) && !errorMessage">
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
            selectedDescription: null,
            token: '',
            user: null,
            errorMessage: '',
            goHomeButton: false,
            bigpk: {
                p: null,
                g: null,
                y: null,
            },
            successVote: false,
        };
    },    
    created() {
        // check if user has a token
        var cookies = document.cookie.split(';');
        cookies.forEach((cookie) => {
            var pair = cookie.split('=');
            if (pair[0].trim() === 'decide' && pair[1]) {
                this.token = pair[1];
            }
        });
        if (!this.token) {
            this.errorMessage = 'No se ha iniciado sesión';
            setTimeout(() => {
                this.$router.push('/login');
            }, 2000); 
        } else {
            this.getUser();
        }
    },
    methods: {
        redirectToHomePage() {
            window.location.href = '/';
        },

        getUser() {
            fetch(import.meta.env.VITE_API_URL+'/gateway/authentication/getuser/', {
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
                    return response.json();
                } else {
                    throw new Error('Error obteniendo el usuario');
                }
            })
            .then((data) => {
                this.user = data;
                this.getVoting();
            })
            .catch((error) => {
                this.errorMessage = error.message;
                setTimeout(() => {
                    this.$router.push('/login');
                }, 2000);  
            });
        },
        getVoting() {
            fetch(import.meta.env.VITE_API_URL + '/voting/' + this.$route.params.id + '/stringkeys')
            .then((response) => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Votación no encontrada');
                }
            })
            .then((data) => {
                var voting_data = JSON.parse(data.voting);
                if (!voting_data.start_date) {
                    throw new Error('Votación no iniciada');
                }
                if (voting_data.end_date) {
                    throw new Error('Votación finalizada');
                }

                window.ElGamal.BITS = data.KEYBITS;
                this.bigpk.p = window.BigInt.fromJSONObject(voting_data.pub_key.p.toString());
                this.bigpk.g = window.BigInt.fromJSONObject(voting_data.pub_key.g.toString());
                this.bigpk.y = window.BigInt.fromJSONObject(voting_data.pub_key.y.toString());

                setTimeout(() => {
                    this.voting = voting_data;
                }, 500);
                
            })
            .catch((e) => {
                if (!this.errorMessage) {
                    setTimeout(() => {
                        this.errorMessage = e.message;
                        this.goHomeButton = true;
                    }, 500); 
                }
            });
        },
        encrypt() {
            var bigmsg = window.BigInt.fromJSONObject(this.selectedOption.toString());
            var cypher = window.ElGamal.encrypt(this.bigpk, bigmsg);
            return cypher;
        },
        vote() {
            var v = this.encrypt();
            fetch(import.meta.env.VITE_API_URL + '/gateway/store/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token ' + this.token,
                },
                body: JSON.stringify({
                    voting: this.voting.id,
                    voter: this.user.id,
                    token: this.token,
                    vote: {
                        a: v.alpha.toString(),
                        b: v.beta.toString(),
                    },
                }),
            })
            .then((response) => {
                if (response.ok) {
                    return this.successVote = true;
                } else if (response.status == 401) {
                    throw new Error('No tiene permisos para participar en esta votación');
                } else {
                    throw new Error('Error al votar');
                }
                
            })
            .catch((e) => {
                this.errorMessage = e.message;
                this.goHomeButton = true;
            });
        }
    },
};
</script>

<style scoped>
    .error-screen {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .error-message {
        color: lightcoral;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        text-align: center;
        font-size: 2em;
    }

    ul {
        list-style-type: none;
        padding: 0;
        text-align: left;
        margin: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    li {
        margin-bottom: 10px;
        padding: 10px;
        background-color: grey;
        border-radius: 5px;
        border: 1px solid #dee2e6;
        width: 50%;
        box-sizing: border-box;
    }

    li:hover {
        cursor: pointer;
        background-color: #dee2e6;
    }

    li.selected {
        background-color: #007bff;
        color: white;
    }

    .voting-container {
        min-width: 1000px;
        align-items: flex-start;
        justify-content: top center;
    }

    .question {
        text-align: center;
        padding-top: 40px;
    }
    .vote-button {
        background-color: lightgreen;
        color: rgb(0, 0, 0);
        border-radius: 5px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Añade una sombra al botón */
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        width: 30%;
        align-self: center;
        margin-top: 30px;
    }
</style>