<template>
    <div class="form-div" v-if="form">
        <h1>Decide Admin Login</h1>
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
        <button class="login-button" :disabled="isButtonDisabled" type="submit">INICIAR SESIÓN</button>
      </form>
    </div>
    <p v-else>Cargando...</p>
</template>

<script>
export default {
    name: 'AdminLogin',
    data() {
        return {
            username: '',
            password: '',
            sessionid: '',
            error: '',
            success: '',
            form: false,
            };
    },
    mounted() {
        this.form = false,
        this.isUserLogged();
    },
    methods: {
            login() {
                this.error = '';
                this.success = '';
                var headers = {
                    'Content-Type': 'application/json',
                }
                fetch(import.meta.env.VITE_API_URL + '/authentication/login-auth/', {
                    method: 'POST',
                    headers: headers,
                    credentials: 'include',
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
                    if (data) {
                        this.getUser();
                    } else  {
                        throw new Error('Usuario o contraseña incorrectos');
                    }
                })
                .catch((error) => {
                    this.error = error.message;
                    console.log(error.message);
                });
            },
            getUser() {
                fetch(import.meta.env.VITE_API_URL + '/authentication/admin-auth/', {
                    method: 'GET',
                    credentials: 'include',
                })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        this.form = true;
                        throw new Error('Error obteniendo el usuario');
                    }
                })
                .then((data) => {
                    if (data.user_data.is_staff) {
                        this.success = `Bienvenido ${data.user_data.username}`;
                        setTimeout(() => {
                            this.$router.push('/');
                        }, 2000);   
                    } else {
                        this.form = true;
                        throw new Error('Usuario o contraseña incorrectos');
                    }
                })
                .catch((error) => {
                    this.error = error.message;
                    console.log(error.message);
                });
        },
        isUserLogged() {
            fetch(import.meta.env.VITE_API_URL + '/authentication/admin-auth/', {
                    method: 'GET',
                    credentials: 'include',
                })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        this.form = true;
                    }
                })
                .then((data) => {
                    if (data.user_data.is_staff) {
                        setTimeout(() => {
                            this.$router.push('/');
                        }, 2000); 
                    } else {
                        this.form = true;
                    }
                })
                .catch(() => {
                   this.form = true;
                });
        }
    } 
};

</script>

<style scoped>
form {
        display: flex;
        flex-direction: column;
        align-self: center;
    }
    label {
        display: block;
        margin-bottom: 5px;
        text-align: left;
        color: #000000; /* Cambia esto al color que prefieras */
        font-family: Arial, Helvetica, sans-serif;
    }
    input {
        height: 25px;
        margin-bottom: 20px;
        border-radius: 5px;
        border: 2px solid rgb(0, 0, 0); /* Cambia esto al color que prefieras */
        width: 100%;
        height: 35px;
        box-sizing: border-box;
        text-align: left;
        padding-left: 10px;
        float: left;
        
    }
    .form-div {
        display: flex;
        flex-direction: column;
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
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .success-message {
        color: green;
        background-color: rgb(199, 255, 199);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .login-button {
        background-color: #2196F3;
        color: rgb(255, 255, 255);
        border-radius: 5px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Añade una sombra al botón */
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        width: 50%;
        align-self: center;
        margin-top: 30px;
    }
    .login-button:active {
        background-color: #0a7bd0; /* Cambia esto a tu color preferido */
        color: #ffffff;
    }

    .login-button:hover {
        background-color: #0a8be6; /* Cambia esto a tu color preferido */
        color: #ffffff;
    }

    .login-button:disabled {
        background-color: #cccccc; /* Cambia esto a tu color preferido */
        color: #888888;
    }
</style>