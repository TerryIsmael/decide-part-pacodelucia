<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-lg-6 rounded border p-4">
                <div class="text-center mb-4">
                    <h2 class="text-success">Sign Up</h2>
                    <hr class="my-4">
                </div>

                <form action="/authentication/register/" method="POST">
                    <!-- Username -->
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input required type="text" name="username" id="username"
                            value="" class="form-control">
                    </div>

                    <!-- Email -->
                    <div class="form-group">
                        <label for="email">Email</label>
                        <input required type="email" name="email" id="email"
                            value="" class="form-control" placeholder="example@gmail.com">
                    </div>

                    <!-- Password -->
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" name="password" id="password" class="form-control">
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
            voting: null,
            selectedOption: null,
        };
    },

    methods: {
        register() {
            console.log("TEST");
        }
    },
};
</script>

<style scoped>
/* Tus estilos van aquí */
</style>