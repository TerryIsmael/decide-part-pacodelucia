<script>
    import NavbarAdmin from './NavbarAdmin.vue';
</script>

<template>
    <NavbarAdmin/>
    <div class="principal_div" >
        <h2>Inicio de administrador</h2>
        <div class="adjusted">
            <a href="/admin/voting"> <button>Votaciones</button> </a>
            <a href="/admin/question"> <button>Preguntas</button> </a>
            <a href="/admin/auth"> <button>Autoridades</button> </a>
            <a href="/admin/census"> <button>Censos</button> </a>
            <a href="/admin/user"> <button>Usuarios</button> </a>
            <a href="/admin/userdata"> <button>Datos de usuarios</button> </a>
            <a href="/admin/vote"> <button>Votos</button> </a>
            <a href="/admin/authtoken"> <button>Tokens de autorización</button> </a>
            <a href="/admin/mixnet" class="adjusted"> <button>Mixnet</button> </a>
        </div>
    </div>
</template>
  
<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: auto;
    margin-top: 10px;
}

.adjusted {
    width: 100%;
    margin-top: 10px;
}

.adjusted a {
    display: block;
    margin-bottom: 10px;
}
</style>