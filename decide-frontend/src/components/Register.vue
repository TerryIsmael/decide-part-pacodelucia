<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-lg-6 rounded border p-4">
                <div class="text-center mb-4">
                    <h2 class="text-success">Sign Up</h2>
                    <hr class="my-4">
                </div>

                <form @submit.prevent="register">
                    <!-- Username -->
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input v-model="username" type="text"   class="form-control" required>
                    </div>

                    <!-- Email -->
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input v-model="email" type="email"  class="form-control" placeholder="example@gmail.com" required>
                    </div>

                    <!-- Password -->
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input v-model="password" type="password" class="form-control" required>
                    </div>

                    <hr class="my-4">

                    <button type="submit" class="btn btn-success btn-block">Create Account</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>

export default {

    name: 'Register',
    data() {
        return {
            username: '',
            email: '',
            password: '',
        };
    },

    methods: {
    async register() {
        try {
            const response = await fetch('http://localhost:8000/authentication/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: this.username,
                    email: this.email,
                    password: this.password,
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
            console.log(data);
        } catch (error) {
            // Manejar errores de red u otros errores
            console.error('Error:', error);
        }
    },
},

    
};
</script>

<style scoped>
/* Tus estilos van aquí */
</style>
