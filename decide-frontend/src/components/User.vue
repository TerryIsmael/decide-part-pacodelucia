<script>
import { ref, onMounted, inject } from "vue";
import User from "../../models/User.js";

export default {
    setup() {
        const users = ref({});
        const selectedUser = ref(null);
        const New = ref("New");
        const editing = ref(false);
        const newUser = ref(new User());
        const loading = ref(false);
        const newUserError = ref(null);
        const logged = inject("logged");
        const navBarLoaded = inject('navBarLoaded')

        const init = async () => {
            while (!navBarLoaded.value) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            navBarLoaded.value = false;
            if (logged.value) {
                //Init functions
                fetchUsers();
            }
        }

        onMounted(init);

        const fetchUsers = async () => {
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/authentication/user/front/",
                    {
                        method: "GET",
                        credentials: "include",
                    });
                const data = await response.json();
                users.value = data;
            } catch (error) {
                console.error("Error:", error);
            }
        };

        const changeEditing = async (newValue) => {
            if (newValue == true && selectedUser.value != "New") {
                newUser.value = { ...users.value.find(x => x.id == selectedUser.value) };
            } else {
                newUser.value = new User();
            }
            editing.value = newValue;
            newUserError.value = null;
        };

        const deleteUser = async (id) => {
            const userDelete = {
                id: id,
            };

            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/authentication/user/front/",
                    {
                        method: "DELETE",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        credentials: "include",
                        body: JSON.stringify(userDelete),
                    }
                );
            } catch (error) {
                console.error("Error:", response.status, error.json());
            }
            fetchUsers();
        }

        const saveUser = async () => {

            if (newUser.value.id == undefined && (newUser.value.password == undefined || newUser.value.password.trim() == "")) {
                newUserError.value = "El nombre de usuario y la contraseña no pueden estar vacíos o estar formadas por espacios en blanco";
                return;
            }

            if (newUser.value.username == undefined || newUser.value.username.trim() == ""){
                newUserError.value = "El nombre de usuario no puede estar vacío";
                return;
            }

            const userPost = {
                id: newUser.value.id,
                username: newUser.value.username.trim(),
                password: newUser.value.password?.trim(),
                first_name: newUser.value.first_name?.trim(),
                last_name: newUser.value.last_name?.trim(),
                email: newUser.value.email,
                is_active: newUser.value.is_active,
                is_staff: newUser.value.is_staff,
                is_superuser: newUser.value.is_superuser,
            };

            const sameUsernames = users.value.filter(x => x.username == newUser.value.username);

            if (sameUsernames != undefined && sameUsernames.filter(x => x.id != newUser.value.id).length > 0) {
                newUserError.value = "Ya existe un usuario con ese nombre";
                return;
            }

            editing.value = false;
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/authentication/user/front/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                    body: JSON.stringify(userPost),
                });
                newUserError.value = null;
            } catch (error) {
                console.error("Error:", response.status, error.json());
            }

            newUser.value = new User();
            await fetchUsers();
        };

        const changeSelected = (id) => {
            selectedUser.value = selectedUser.value === id ? null : id;
            newUserError.value = null;
        };

        

        return {
            users,
            selectedUser,
            New,
            editing,
            newUser,
            loading,
            newUserError,
            changeSelected,
            changeEditing,
            saveUser,
            deleteUser,
            fetchUsers,
        };
    },
};
</script>

<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
        integrity="nueva-cadena-de-integridad" crossorigin="anonymous">
    <div>
        <h2>Listado de usuarios</h2>
        <ul>
            <button class="little-button adjusted" style="margin-bottom: 10px;"
                @click="changeSelected(New), changeEditing(true)"> Nuevo usuario </button>

            <div v-if="selectedUser == 'New' && editing == true">
                <form @submit.prevent="saveUser">
                    <div>
                        <p class="bold" style="color:rgb(211, 91, 91)">{{newUserError}}</p>
                    </div>
                    <div>
                        <label for="username">Nombre de usuario: </label>
                        <input type="text" id="username" v-model="newUser.username" required />
                        <label for="password">Contraseña: </label>
                        <input type="password" id="password" v-model="newUser.password" required />
                        <label for="email_address">Email: </label>
                        <input type="email" id="email_address" v-model="newUser.email" />
                        <label for="first_name">Nombre: </label>
                        <input type="text" id="first_name" v-model="newUser.first_name" />
                        <label for="last_name">Apellido: </label>
                        <input type="text" id="last_name" v-model="newUser.last_name" />
                        <label for="is_active">Activo: </label>
                        <input type="checkbox" id="is_active" v-model="newUser.is_active" />
                        <label for="is_staff">Staff: </label>
                        <input type="checkbox" id="is_staff" v-model="newUser.is_staff" />
                        <label for="is_superuser">Superusuario: </label>
                        <input type="checkbox" id="is_superuser" v-model="newUser.is_superuser" />
                    </div>
                    <div>
                        <button class="little-button adjusted" type="submit"> Guardar </button>
                        <button class="little-button adjusted" @click="changeEditing(false)"> Cancelar </button>
                    </div>
                </form>
            </div>

            <li v-for="user in users" :key="user.id">
                <h3>
                    <button @click="changeSelected(user.id); changeEditing(false);">{{ user.username }}</button>
                </h3>
                <div v-if="selectedUser === user.id">
                    <p><span class="bold">Id:</span> {{ user.id }}</p>
                    <div v-if="!editing">
                        <p><span class="bold">Nombre de usuario: </span>{{ user.username }}</p>
                        <p><span class="bold">Email: </span>{{ user.email }}</p>
                        <p><span class="bold">Nombre: </span>{{ user.first_name }}</p>
                        <p><span class="bold">Apellido: </span>{{ user.last_name }}</p>
                        <p><span class="bold">Activo: </span>{{ user.is_active }}</p>
                        <p><span class="bold">Staff: </span>{{ user.is_staff }}</p>
                        <p><span class="bold">Superusuario: </span>{{ user.is_superuser }}</p>
                        <button class="little-button adjusted" @click="changeEditing(true)"> Editar </button>
                        <button class="little-button deleteButton adjusted" @click="deleteUser(user.id)"> Eliminar </button>
                    </div>

                    <div v-else>
                        <form @submit.prevent="saveUser">
                            <div>
                                <p class="bold" style="color:rgb(211, 91, 91)">{{newUserError}}</p>
                            </div>
                            <div>
                                <label for="username">Nombre de usuario: </label>
                                <input type="text" id="username" v-model="newUser.username" required />
                                <label for="password">Contraseña (no rellenar si no se desea cambiar): </label>
                                <input type="password" id="password" v-model="newUser.password" />
                                <label for="email_address">Email: </label>
                                <input type="email" id="email_address" v-model="newUser.email" />
                                <label for="first_name">Nombre </label>
                                <input type="text" id="first_name" v-model="newUser.first_name" />
                                <label for="last_name">Apellido </label>
                                <input type="text" id="last_name" v-model="newUser.last_name" />
                                <label for="is_active">Activo </label>
                                <input type="checkbox" id="is_active" v-model="newUser.is_active" />
                                <label for="is_staff">Staff </label>
                                <input type="checkbox" id="is_staff" v-model="newUser.is_staff" />
                                <label for="is_superuser">Superusuario </label>
                                <input type="checkbox" id="is_superuser" v-model="newUser.is_superuser" />
                            </div>
                            <div>
                                <button class="little-button adjusted" type="submit"> Guardar </button>
                                <button class="little-button adjusted" @click="changeEditing(false)"> Cancelar </button>
                            </div>
                        </form>
                    </div>
                </div>
            </li>
        </ul>
    </div>
</template>

<style scoped>
#auths {
    background-color: #3b3b3b;
    height: 60px;
    margin-bottom: 20px;
    padding: 5px;
    border-radius: 5px;
    border: 2px solid grey;
    width: 67%;
}

.deleteButton {
    background-color: rgb(211, 91, 91);
    width: auto;
}

button:disabled {
    background-color: grey;
}

.adjusted {
    width: auto;
}

.error {
    background-color: rgb(211, 91, 91);
    color: white;
    display: block;
    border-radius: 8px;
    width: 60%;
    margin-left: auto;
    margin-right: auto;
}
</style>