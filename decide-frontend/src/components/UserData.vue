<script>
import { ref, onMounted, inject } from "vue";
import UserData from "../../models/UserData.js";

export default {
    setup() {
        const userDatas = ref([]);
        const users = ref([]);
        const newUserData = ref(new UserData());
        const editing = ref(false);
        const newUserDataError = ref(null);
        const selectedUserData = ref(null);
        const navBarLoaded = inject("navBarLoaded");
        const logged = inject("logged");
        const New = "New";
        const minYear = new Date().getFullYear() - 100;
        const maxYear = new Date().getFullYear();

        const init = async () => {
            while (!navBarLoaded.value) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            navBarLoaded.value = false;
            if (logged.value) {
                //Init functions
                fetchData();
            }
        }

        onMounted(init);

        const fetchData = async () => {
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
            try {
                const response2 = await fetch(import.meta.env.VITE_API_URL + "/census/user-details/",
                    {
                        method: "GET",
                        credentials: "include",
                    });
                const data2 = await response2.json();
                userDatas.value = data2;
            } catch (error) {
                console.error("Error:", error);
            }
        };

        const changeEditing = async (newValue) => {
            if (newValue == true && selectedUserData.value != "New") {
                newUserData.value = { ...userDatas.value.find(x => x.id == selectedUserData.value) };
            } else {
                newUserData.value = new UserData();
            }
            editing.value = newValue;
            newUserDataError.value = null;
        };

        const saveUserData = async () => {

            if (newUserData.value.born_year < new Date().getFullYear() - 100 || newUserData.value.born_year > new Date().getFullYear()){
                newUserDataError.value = `El año de nacimiento debe estar entre ${new Date().getFullYear() - 100} y ${new Date().getFullYear()}`;
                return;
            }

            const userDataPost = {
                voter_id : newUserData.value.voter_id,
                born_year : newUserData.value.born_year,
                country : newUserData.value.country,
                religion : newUserData.value.religion,
                gender : newUserData.value.gender,
                civil_state : newUserData.value.civil_state,
                works : newUserData.value.works,
            };
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/census/user-details/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include",
                    body: JSON.stringify(userDataPost),
                });
                newUserDataError.value = null;
            } catch (error) {
                console.error("Error:", response.status, error.json());
            }

            newUserData.value = new UserData();
            editing.value = false;
            await fetchData();
        };

        const changeSelected = (id) => {
            selectedUserData.value = selectedUserData.value === id ? null : id;
            newUserDataError.value = null;
            editing.value = false;
        };

        const parseReligion = (religion) =>{
            switch (religion){
                case "CH":
                    return "Cristianismo";
                case "IS":
                    return "Islam";
                case "HI":
                    return "Hinduismo";
                case "BU":
                    return "Budismo";
                case "AG":
                    return "Agnóstico";
                case "AT":
                    return "Ateísmo";
                case "OT":
                    return "Otras";
            }
        }

        const parseGender = (gender) =>{
            switch (gender){
                case "MA":
                    return "Masculino";
                case "FE":
                    return "Femenino";
                case "NB":
                    return "No binario";
                case "NP":
                    return "Sin respuesta";
            }
        }

        const parseCivilState = (civil_state) =>{
            switch (civil_state){
                case "SI":
                    return "Soltero/a";
                case "MA":
                    return "Casado/a";
                case "DI":
                    return "Divorciado/a";
                case "WI":
                    return "Viudo/a";
            }
        }

        const parseWorks = (works) =>{
            switch (works){
                case "ST":
                    return "Estudiante";
                case "WO":
                    return "Trabajador/a";
                case "UN":
                    return "Desempleado/a";
            }
        }

        const findVoter = (voter_id) =>{
            return users.value.find(x => x.id == voter_id);
        }

        return {
            userDatas,
            users,
            newUserData,
            editing,
            newUserDataError,
            selectedUserData,
            New,
            minYear,
            maxYear,
            changeEditing,
            saveUserData,
            changeSelected,
            parseReligion,
            parseGender,
            parseCivilState,
            parseWorks,
            findVoter,
        };
    },
};
</script>

<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
        integrity="nueva-cadena-de-integridad" crossorigin="anonymous">
    <div>
        <h2>Listado de datos de usuarios</h2>
        <ul>
            <button class="little-button adjusted" style="margin-bottom: 10px;"
                @click="changeSelected(New), changeEditing(true)"> Nuevos datos de usuario </button>

            <div v-if="selectedUserData == 'New' && editing == true">
                <form @submit.prevent="saveUserData">
                    <div>
                        <p class="bold" style="color:rgb(211, 91, 91)">{{newUserDataError}}</p>
                    </div>
                    <div>
                        <label for="voter_id">Usuario: </label>
                        <select id="voter_id" v-model="newUserData.voter_id" required>
                            <option v-for="user in users" :key="user.id" :value="user.id">{{ user.username }}</option>
                        </select>
                        <label for="born_year">Año de nacimiento:</label>
                        <input type="number" id="born_year" v-model="newUserData.born_year" required />
                        <label for="country">País:</label>
                        <input type="text" id="country" v-model="newUserData.country" required />
                        <label for="religion">Religión:</label>
                        <select v-model="newUserData.religion" required>
                            <option value="CH">Cristianismo</option>
                            <option value="IS">Islam</option>
                            <option value="HI">Hinduismo</option>
                            <option value="BU">Budismo</option>
                            <option value="AG">Agnóstico</option>
                            <option value="AT">Ateísmo</option>
                            <option value="OT">Otras</option>
                        </select>
                        <label for="gender">Género:</label>
                        <select v-model="newUserData.gender" required>
                            <option value="MA">Masculino</option>
                            <option value="FE">Femenino</option>
                            <option value="NB">No binario</option>
                            <option value="NP">Sin respuesta</option>
                        </select>
                        <label for="civil_state">Estado civil:</label>
                        <select v-model="newUserData.civil_state" required>
                            <option value="SI">Soltero/a</option>
                            <option value="MA">Casado/a</option>
                            <option value="DI">Divorciado/a</option>
                            <option value="WI">Viudo/a</option>
                        </select>
                        <label for="works">Trabaja:</label>
                        <select v-model="newUserData.works" required>
                            <option value="ST">Estudiante</option>
                            <option value="WO">Trabajador/a</option>
                            <option value="UN">Desempleado/a</option>
                        </select>
                    </div>
                    <div>
                        <button class="little-button adjusted" type="submit"> Guardar </button>
                        <button class="little-button adjusted" @click="changeEditing(false)"> Cancelar </button>
                    </div>
                </form>
            </div>

            <li v-for="userData in userDatas" :key="userData.id">
                <h3>
                    <button @click="changeSelected(userData.id); changeEditing(false);">{{ findVoter(userData.voter_id).username }}</button>
                </h3>
                <div v-if="selectedUserData === userData.id">
                    <p><span class="bold">Id:</span> {{ userData.id }}</p>
                    <p><span class="bold">Votante: </span>{{ findVoter(userData.voter_id).username }}</p>
                    <div v-if="!editing">
                        <p><span class="bold">Año de nacimiento: </span>{{ userData.born_year }}</p>
                        <p><span class="bold">País: </span>{{ userData.country }}</p>
                        <p><span class="bold">Religión: </span>{{ parseReligion(userData.religion) }}</p>
                        <p><span class="bold">Género: </span>{{parseGender(userData.gender)}}</p>
                        <p><span class="bold">Estado civil: </span>{{parseCivilState(userData.civil_state)}}</p>
                        <p><span class="bold">Trabaja: </span>{{parseWorks(userData.works)}}</p>
                        <button class="little-button adjusted" @click="changeEditing(true)"> Editar </button>
                    </div>
                    <div v-else>
                        <form @submit.prevent="saveUserData">
                            <div>
                                <p class="bold" style="color:rgb(211, 91, 91)">{{newUserDataError}}</p>
                            </div>
                            <div>
                                <label for="voter_id">Usuario: </label>
                                <label for="born_year">Año de nacimiento:</label>
                                <input type="number" :min="minYear" :max="maxYear" id="born_year" v-model="newUserData.born_year" required />
                                <label for="country">País:</label>
                                <input type="text" id="country" v-model="newUserData.country" required />
                                <label for="religion">Religión:</label>
                                <select v-model="newUserData.religion" required>
                                    <option value="CH">Cristianismo</option>
                                    <option value="IS">Islam</option>
                                    <option value="HI">Hinduismo</option>
                                    <option value="BU">Budismo</option>
                                    <option value="AG">Agnóstico</option>
                                    <option value="AT">Ateísmo</option>
                                    <option value="OT">Otras</option>
                                </select>
                                <label for="gender">Género:</label>
                                <select v-model="newUserData.gender" required>
                                    <option value="MA">Masculino</option>
                                    <option value="FE">Femenino</option>
                                    <option value="NB">No binario</option>
                                    <option value="NP">Sin respuesta</option>
                                </select>
                                <label for="civil_state">Estado civil:</label>
                                <select v-model="newUserData.civil_state" required>
                                    <option value="SI">Soltero/a</option>
                                    <option value="MA">Casado/a</option>
                                    <option value="DI">Divorciado/a</option>
                                    <option value="WI">Viudo/a</option>
                                </select>
                                <label for="works">Trabaja:</label>
                                <select v-model="newUserData.works" required>
                                    <option value="ST">Estudiante</option>
                                    <option value="WO">Trabajador/a</option>
                                    <option value="UN">Desempleado/a</option>
                                </select>
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