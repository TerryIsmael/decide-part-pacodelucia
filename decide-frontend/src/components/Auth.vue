<script>
import { ref, onMounted, inject } from "vue";
import Auth from "../../models/Auth.js";

export default {
    setup() {
        const auths = ref([]);
        const selectedAuth = ref(null);
        const editing = ref(false);
        const newAuth = ref(new Auth());
        const New = "New"
        const logged = inject("logged");
        const navBarLoaded = inject('navBarLoaded')
        
        const init = async () => {
            while (!navBarLoaded.value) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            navBarLoaded.value = false; 
            if (logged.value) {
                //Init functions
                fetchAuths();
            }
        }

        onMounted(init);

        const fetchAuths = async () => {
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/base/auth", {
                    method: "GET",
                    credentials: "include",
                }
                );
                const data = await response.json();
                auths.value = data.sort((a,b) => a.id-b.id);
            } catch (error) {
                console.error("Error:", error);
            }
        };

        const changeSelected = (id) => {
            selectedAuth.value = selectedAuth.value === id ? null : id;
        };

        const deleteAuth = async (id) => {
            try {
                const jsonId={
                    id: id
                }
                const response = await fetch(
                    `http://localhost:8000/base/auth/`,
                    {
                        method: "DELETE",
                        credentials: "include",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(jsonId),
                    }
                );
                await fetchAuths();
            } catch (error) {
                console.error("Error:", error);
            }
        };

        const saveAuth = async () => {
            editing.value = false;
            const authPost = {
                id: newAuth.value.id,
                name: newAuth.value.name,
                url: newAuth.value.url,
                me: newAuth.value.me,
            };
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/base/auth/", {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(authPost),
                });
            } catch (error) {
                console.error("Error:", response.status, error.json());
            }

            newAuth.value = new Auth();
            fetchAuths();
        };
        
        const changeEditing = (value) => {
            editing.value = value;
            if (value && selectedAuth.value !== New) {
                newAuth.value = auths.value.find((auth) => auth.id === selectedAuth.value);
            } else {
                newAuth.value = new Auth();
            }
        };
        
        

        return {
            auths,
            selectedAuth,
            editing,
            newAuth,
            New,
            changeSelected,
            deleteAuth,
            saveAuth,
            changeEditing,
        };
    },
};
</script>

<template>
    <div>
        <h2>Listado de Autoridades</h2>

        <button class="little-button" @click="changeSelected(New); changeEditing(true)">
            Nueva autoridad
        </button>

        <div v-if="selectedAuth == New && editing == true">
            <form @submit.prevent="saveAuth">
                <label for = "name">Nombre</label>
                <input required type="text" id="name" v-model="newAuth.name"/>
                <label for = "url">URL</label>
                <input required type="text" pattern="https?://.+" id="url" v-model="newAuth.url" placeholder="URL" />
                <label for = "me">Yo</label>
                <input type="checkbox" id="me" v-model="newAuth.me"/>
                <div>
                    <button class="little-button" type="submit">Añadir</button>
                </div>
            </form>
        </div>

        <ul>
            <li v-for="auth in auths" :key="auth">
                <h3>
                    <button @click="changeSelected(auth.id), changeEditing(false)">
                       {{ auth.name }}
                    </button>
                </h3>
                <div v-if="selectedAuth == auth.id">
                    <div v-if="editing">
                        <form @submit.prevent="saveAuth">
                            <label for = "name">Nombre</label>
                            <input required type="text" id="name" v-model="newAuth.name"/>
                            <label for = "url">URL</label>
                            <input required type="text" pattern="https?://.+" id="url" v-model="newAuth.url" placeholder="URL" />
                            <label for = "me">Yo</label>
                            <input type="checkbox" id="me" v-model="newAuth.me"/>
                            <div>
                                <button class="little-button" @click="changeEditing(false)">Cancelar</button>
                                <button class="little-button" type="submit">Guardar</button>
                            </div>
                        </form>
                    </div>
                    <div v-else>
                        <p><span class="bold">Id:</span> {{ auth.id }}</p>
                        <p><span class="bold">Nombre:</span> {{ auth.name }}</p>
                        <p><span class="bold">URL:</span> {{ auth.url }}</p>
                        <p><span class="bold">Yo:</span> {{ auth.me }}</p>
                        <button class="little-button" @click="changeEditing(true)">Editar</button>
                        <button class="little-button delete_button" @click="deleteAuth(auth.id)">Eliminar</button>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.big-n {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    align-items: center;
}

.big-n>input {
    height: 30px;
    margin-bottom: 20px;
    padding: 5px;
    border-radius: 5px;
    border: 2px solid grey;
    width: 300%;
}

.big-container {
    display: flex;
    flex-direction: column;
}

.little-button {
    width: auto;
}

.delete_button{
    background-color: rgb(211, 91, 91);
}

ul ul li h3>button {
    margin-left: 20px;
    list-style-type: square;
    background-color: rgb(1, 88, 88);
}
</style>