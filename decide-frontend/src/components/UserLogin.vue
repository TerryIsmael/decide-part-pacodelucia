<script>
import { ref, onMounted, inject } from "vue";

export default {
    setup() {
        const username = inject('userUsername');
        const error = ref('');
        const success = ref('');
        const logged = inject('logged');
        const form = ref(false);
        const token = ref('');
        const user = ref('');
        const password = ref('');

       

        const isButtonDisabled = () => {
            return user.value === '' || password.value === '';
        }
        
        const init = () => {
            var cookies = document.cookie.split(';');
            cookies.forEach((cookie) => {
                var pair = cookie.split('=');
                if (pair[0].trim() === 'decide' && pair[1]) {
                    token.value = pair[1];
                    isLogged();
                }
            });
            if (!token.value) {
                form.value = true;
            }
        }
        
        const login = () => {
            error.value = '';
            success.value = '';
            var headers = {
                'Content-Type': 'application/json',
            }
            if (token.value) {
                headers['Authorization'] = `Bearer ${token.value}`;
            }
            fetch(import.meta.env.VITE_API_URL + '/gateway/authentication/login/', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({
                    username: user.value,
                    password: password.value,
                }),
            })
                .then((response) => {
                    if (response.ok) {
                        error.value = '';  
                        return response.json();
                    } else {
                        error.value = 'Usuario o contraseña incorrectos';  
                        throw new Error('Usuario o contraseña incorrectos');
                    }
                })
                .then((data) => {
                    token.value = data.token;
                    document.cookie = `decide=${token.value}`;
                    getUser();
                })
                .catch((error) => {
                    error.value = error.message;
                    console.log(error.message);
                });
        }
        
        const getUser = () => {
            fetch(import.meta.env.VITE_API_URL + '/gateway/authentication/getuser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: token.value,
                }),
            })
                .then((response) => {
                    if (response.ok) {
                        logged.value = true;
                        return response.json();
                    } else {
                        throw new Error('Error obteniendo el usuario');
                    }
                })
                .then((data) => {
                    username.value = data.username;
                    success.value = `Bienvenido ${data.username}`;
                    
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                })
                .catch((error) => {
                    error.value = error.message;
                    console.log(error.message);
                });
        }
        
        const isLogged = () => {
            fetch(import.meta.env.VITE_API_URL + '/gateway/authentication/getuser/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    token: token.value,
                }),
            })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Error obteniendo el usuario');
                    }
                })
                .then(() => {
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                })
                .catch((error) => {
                    setTimeout(() => {
                        form.value = true;
                        error.value = error.message
                    }, 1000);
                });
        }

        onMounted(init)

        return {
            username,
            logged,
            password,
            token,
            error,
            success,
            form,
            user,
            isLogged,
            login,
            getUser,
            isButtonDisabled,
        };
    },
} 

</script>


<template>
    <div class="form-div" v-if="form">
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
                <input type="text" id="username" v-model="user" required>
            </div>
            <div>
                <label for="password">Contraseña:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button class="login-button"  type="submit">INICIAR SESIÓN</button>
        </form>
    </div>
    <div v-else>
        <h1>Iniciando sesión...</h1>
    </div>
</template>


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
    color: #000000;
    /* Cambia esto al color que prefieras */
    font-family: Arial, Helvetica, sans-serif;
}

input {
    height: 25px;
    margin-bottom: 20px;
    border-radius: 5px;
    border: 2px solid rgb(0, 0, 0);
    /* Cambia esto al color que prefieras */
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

.form-div>form {
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
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
    /* Añade una sombra al botón */
    padding: 10px;
    font-size: 16px;
    cursor: pointer;
    width: 50%;
    align-self: center;
    margin-top: 30px;
}

.login-button:active {
    background-color: #0a7bd0;
    /* Cambia esto a tu color preferido */
    color: #ffffff;
}

.login-button:hover {
    background-color: #0a8be6;
    /* Cambia esto a tu color preferido */
    color: #ffffff;
}

.login-button:disabled {
    background-color: #cccccc;
    /* Cambia esto a tu color preferido */
    color: #888888;
}
</style>