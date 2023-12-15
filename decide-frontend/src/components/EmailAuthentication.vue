<template>
    <div class="form-div">
        <h1>Decide Registro</h1>
        <form @submit.prevent="register">
            <!-- Username -->
            <div class="form-group">
                <label for="username">Username</label>
                <input v-model="username" type="text" class="form-control" required>
            </div>

            <!-- Clave -->
            <div class="form-group">
                <label for="clave">Clave</label>
                <input v-model="clave" type="clave" class="form-control" required>
            </div>

            <div v-if="success" class="success-message">
                {{ success }}
            </div>

            <div v-if="error" class="error-message">
                {{ error }}
            </div>

            <hr class="my-4">

            <button type="submit" class="register-button">Autenticar Cuenta</button>
        </form>
    </div>
</template>

<script>

export default {

    name: 'Register',
    data() {
        return {
            username: '',
            clave: '',
            success: '',
            error: '',
        };
    },
    methods: {
    async register() {
        try {
            const response = await fetch(import.meta.env.VITE_API_URL+'/authentication/authEmail/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    clave: this.clave,
                }),
            });

            if (!response.ok) {
                if (response.status === 400) {
                    const errorData = await response.json();
                    // Manejar los errores de validación y presentar mensajes al usuario
                    console.error('Error 400:', errorData);
                } else {
                    // Manejar otros errores HTTP
                    console.error('Error:', response.status, response.statusText);
                }
                return;
            }

            const data = await response.json();

            // Manejar la respuesta como sea necesario
            this.success = "Creación de Cuenta Confirmada!";
            console.log(data);
        } catch (error) {
            // Manejar errores de red u otros errores
            this.error = `Error: ${error.message}`;
            console.error('Error:', error);
        }
    },
},

    
};
</script>

<style scoped>
    h1{
        align-self: center;
        font-family:'Courier New', Courier, monospace;
    }
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
    
    .register-button {
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
    .register-button:active {
        background-color: #0a7bd0; /* Cambia esto a tu color preferido */
        color: #ffffff;
    }

    .register-button:hover {
        background-color: #0a8be6; /* Cambia esto a tu color preferido */
        color: #ffffff;
    }

    .success-message {
        color: green;
        background-color: rgb(199, 255, 199);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .error-message {
        color: rgb(0, 0, 0);
        background-color: rgb(255, 196, 196);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
