<template>
    <div v-if="voting && user">
        <h1>{{ voting.name }}</h1>
        <p>{{ voting.desc }}</p>
        <p>Question: {{ voting.question.desc }}</p>
        <ul>
            <li v-for="option in voting.question.options" :key="option.number">
                <input type="radio" :id="'q'+option.number" :value="option.number" v-model="selectedOption">
                <label :for="option.id">{{ option.option }}</label>
            </li>
        </ul>
        <button @click="vote">Vote</button>
    </div>
    <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
        <div v-if="goHomeButton">
            <button @click="$router.push('/')">Go home</button>
        </div>
    </div>
    <div v-if="(!voting || !user) && !errorMessage">
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
    beforeMount() {
        window.ElGamal.BITS = import.meta.env.VITE_KEYBITS;
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
        getUser() {
            fetch(import.meta.env.VITE_API_URL+'gateway/authentication/getuser/', {
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
                
            });
        },
        getVoting() {
            fetch(import.meta.env.VITE_API_URL + 'voting/?id=' + this.$route.params.id)
            .then((response) => response.json())
            .then((data) => {
                if (data.length === 0) {
                    throw new Error('Votación no encontrada');
                }
                setTimeout(() => {
                    this.voting = data[0];
                    this.bigpk.p = window.BigInt.fromJSONObject(this.voting.pub_key.p.toString());
                    this.bigpk.g = window.BigInt.fromJSONObject(this.voting.pub_key.g.toString());
                    this.bigpk.y = window.BigInt.fromJSONObject(this.voting.pub_key.y.toString());
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
            console.log(v);
            fetch(import.meta.env.VITE_API_URL + 'gateway/store/', {
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
                this.successVote = true;
                console.log(response);
                console.log("Voto realizado correctamente")
            })
            .catch((e) => {
                this.errorMessage = "Error al votar: "+e;
                console.log(e);
                console.log("Error al votar");
            });
        }
    },
};
</script>

<style scoped>
    .error-message {
        color: red;
    }

</style>