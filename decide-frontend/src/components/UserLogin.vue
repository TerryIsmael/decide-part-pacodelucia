<template>
    <div class="form-div">
        <h1>Decide Login</h1>
      <form @submit.prevent="login">
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        <div v-if="success" class="success-message">
          {{ success }}
        </div>
        <div>
          <label for="username">Usuario:</label>
          <input type="text" id="username" v-model="username" required>
        </div>
        <div>
          <label for="password">Contraseña:</label>
          <input type="password" id="password" v-model="password" required>
        </div>
        <button type="submit">Iniciar sesión</button>
      </form>
    </div>
</template>

<script>
    export default {
        name: 'UserLogin',
        data() {
            return {
            username: '',
            password: '',
            token: '',
            error: '',
            success: '',
            };
        },
        methods: {
            init() {
                var cookies = document.cookie.split(';');
                cookies.forEach((cookie) => {
                    var pair = cookie.split('=');
                    if (pair[0].trim() === 'decide' && pair[1]) {
                        this.token = pair[1];
                        this.getUser();
                    }
                });
            },
            login() {
                this.error = '';
                this.success = '';
                var headers = {
                    'Content-Type': 'application/json',
                }
                if (this.token) {
                    headers['Authorization'] = `Bearer ${this.token}`;
                }
                fetch('http://localhost:3000/gateway/authentication/login/', {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password,
                    }),
                })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Usuario o contraseña incorrectos');
                    }
                })
                .then((data) => {
                    this.token = data.token;
                    document.cookie = `decide=${this.token}`;
                    this.getUser();
                })
                .catch((error) => {
                    this.error = error.message;
                    console.log(error.message);
                });
            },
            getUser() {
                const user = fetch('http://localhost:3000/gateway/authentication/getuser/', {
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
                    this.success = `Bienvenido ${data.username}`;
                    setTimeout(() => {
                        this.$router.push('/');
                    }, 2000);    
                })
                .catch((error) => {
                    this.error = error.message;
                    console.log(error.message);
                });
            }
        },
    };
</script>

<style scoped>
    form {
        display: flex;
        flex-direction: column;
    }
    label {
        display: block;
        margin-bottom: 5px;
        text-align: left;
        color: #000000; /* Cambia esto al color que prefieras */
    }
    input {
        height: 25px;
        margin-bottom: 20px;
        padding: 5px;
        border-radius: 5px;
        border: 2px solid rgb(0, 0, 0); /* Cambia esto al color que prefieras */
        width: 60%;
    }
    .form-div {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
        overflow: hidden;
    }

    .form-div > form {
        width: 400px;
        padding: 40px;
        border-radius: 5px;
        background-color: rgb(255, 255, 255);
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    }

    .error-message {
        color: rgb(0, 0, 0);
        background-color: rgb(255, 196, 196);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 2px solid #000000;
    }

    .success-message {
        color: green;
        background-color: rgb(199, 255, 199);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 2px solid #000000;
    }

</style>