<template>
    <div class="page-not-found">
        <div class="page-not-found-message">
            <h1>404</h1>
            <h2>Página no encontrada</h2>
            <p>La página que estás buscando no existe.</p>
            <p>Por favor, verifica la URL o haz click en el botón de abajo para volver a la página principal.</p>
            <button @click="this.$router.push('/')">Página Principal</button>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PageNotFound',
};
</script>