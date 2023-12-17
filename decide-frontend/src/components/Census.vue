<script>
import { ref, onMounted, inject } from "vue";
import { Census } from "../../models/Census.js";

export default {
    setup() {
        const censuss = ref({});
        const selectedVoting = ref(null);
        const censusSubList = ref([]);
        const votings = ref([]);
        const allVotings = ref([]);
        const New = ref("New");
        const editing = ref(false);
        const newCensus = ref(new Census());
        const newVoterId = ref("");
        const newVotingId = ref("");
        const newCensusError = ref(null);
        const users = ref([]);
        const usersSubList = ref([]);
        const waiting = ref(null);
        const logged = inject("logged");
        const navBarLoaded = inject('navBarLoaded')
        const filter = ref("");
        const filterTypes = ref(["born_year", "country", "religion", "gender", "civil_state", "works"])
        const filterValues = ref([]);
        const filterValue = ref("");

        const init = async () => {
            while (!navBarLoaded.value) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            navBarLoaded.value = false;
            if (logged.value) {
                //Init functions
                fetchCensuss();
            }
        }

        onMounted(init);

        const fetchCensuss = async () => {
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/census/front/", {
                    method: "GET",
                    credentials: "include",
                });

                const data = await response.json();
                censuss.value = data.sort((a, b) => {
                    if (a.voting_id == b.voting_id) {
                        return a.voter_id - b.voter_id;
                    } else {
                        return a.voting_id - b.voting_id;
                    }
                })
                censuss.value.forEach((census) => {
                    votings.value = [...new Set([...votings.value, census.voting_id])];
                    votings.value = votings.value.sort((a, b) => {
                        return a - b;
                    });
                });
                const response2 = await fetch(import.meta.env.VITE_API_URL + "/authentication/user/front/", {
                    method: "GET",
                    credentials: "include",
                });
                const data2 = await response2.json();
                users.value = data2.sort((a, b) => {
                    return a.id - b.id;
                })
                usersSubList.value = users.value;

                const response3 = await fetch(import.meta.env.VITE_API_URL + "/voting/voting/", {
                    method: "GET",
                    credentials: "include",
                });
                const data3 = await response3.json();
                allVotings.value = data3.sort((a, b) => {
                    return a.id - b.id;
                })

            } catch (error) {
                console.error("Error:", error);
            }
        };

        const changeSelectedVoting = (id) => {
            selectedVoting.value = selectedVoting.value === id ? null : id;
            if (selectedVoting.value != null && selectedVoting.value != New) {
                censusSubList.value = censuss.value.filter((census) => census.voting_id == selectedVoting.value);
            } else {
                censusSubList.value = [];
            }
        };

        const saveCensus = async () => {
            if (selectedVoting.value != "New") {
                newVotingId.value = selectedVoting.value;
            }
            if (newVoterId.value === undefined || newVotingId.value === undefined) {
                newCensusError.value = ("No se puede guardar un censo vacío");
                return;
            }

            if (censuss.value.filter(x => x.voting_id == newVotingId.value).some((census) => census.voter_id == newVoterId.value)) {
                newCensusError.value = ("No se puede volver a añadir el mismo usuario al censo");
                return;
            }

            else
                newCensusError.value = null;

            editing.value = false;

            const newCensus = {
                voting_id: newVotingId.value,
                voters: [newVoterId.value],
            };

            try {
                await fetch(import.meta.env.VITE_API_URL + "/census/front/", {
                    method: "POST",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(newCensus),
                });
            } catch (error) {
                console.error("Error:", error);
            }
            newVoterId.value = "";
            newVotingId.value = "";
            newCensusError.value = null;
            await fetchCensuss();
            censusSubList.value = await censuss.value.filter((census) => census.voting_id == selectedVoting.value);
        };

        const changeEditing = (newValue) => {
            newVotingId.value = "";
            newVoterId.value = "";
            newCensusError.value = null;
            editing.value = newValue;
        };

        const deleteCensus = async (census) => {
            waiting.value = census.voter_id;
            const censusJson = {
                voting_id: census.voting_id,
                voters: [census.voter_id],
            }

            fetch(import.meta.env.VITE_API_URL + "/census/front/", {
                method: "DELETE",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(censusJson),
            });

            await fetchCensuss();
            censusSubList.value = await censuss.value.filter((census) => census.voting_id == selectedVoting.value);
            waiting.value = null;
        };


        const parseFilter = (f)=> {
            switch(f){
                case "born_year":
                    return "Año de nacimiento";
                case "country":
                    return "País";
                case "religion":
                    return "Religión";
                case "gender":
                    return "Género";
                case "civil_state":
                    return "Estado civil";
                case "works":
                    return "Trabajo";
                default:
                    return "Ninguno";
            }
        }

        const parseFilterValue = (f) => {
            switch (f) {
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
                case "MA":
                    return "Masculino";
                case "FE":
                    return "Femenino";
                case "NB":
                    return "No binario";
                case "NP":
                    return "Sin respuesta";
                case "SI":
                    return "Soltero/a";
                case "MA":
                    return "Casado/a";
                case "DI":
                    return "Divorciado/a";
                case "WI":
                    return "Viudo/a";
                case "ST":
                    return "Estudiante";
                case "WO":
                    return "Trabajador/a";
                case "UN":
                    return "Desempleado/a";
            }
        }


        const valuesForFilter = () => {
            filterValue.value = "";

            if (filter.value == "") {
                filterValues.value = [];
                applyFilter();
                return;
            }
            filterValues.value = [];
            switch (filter.value) {
                case "gender":
                    filterValues.value = ["MA", "FE", "NB", "NP"];
                    break;
                case "civil_state":
                    filterValues.value = ["SI", "MA", "DI", "WI"];
                    break;
                case "works":
                    filterValues.value = ["ST", "WO", "UN"];
                    break;
                case "religion":
                    filterValues.value = ["CH", "IS", "HI", "BU", "AG", "AT", "OT"];
                    break;
                default:
                    break;
            }
        };
        const applyFilter = async () => {
            if (filterValue.value == "") {
                usersSubList.value = users.value;
                return;
            }

            try {
                const response = await fetch(import.meta.env.VITE_API_URL + `/census/get-filtered-census?filter=${filter.value}&filter_value=${filterValue.value}`, {
                    method: "GET",
                    credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                    },
                });
                const data = await response.json();
                usersSubList.value = data.users.sort((a, b) => {
                    return a.id - b.id;
                })
            } catch (error) {
                console.error("Error:", error);
            }
        }

        return {
            censuss,
            votings,
            allVotings,
            censusSubList,
            usersSubList,
            New,
            editing,
            users,
            newCensus,
            newVoterId,
            newVotingId,
            newCensusError,
            selectedVoting,
            waiting,
            filter,
            filterTypes,
            filterValues,
            filterValue,
            fetchCensuss,
            changeSelectedVoting,
            saveCensus,
            changeEditing,
            deleteCensus,
            valuesForFilter,
            applyFilter,
            parseFilter,
            parseFilterValue,
        };
    },
};
</script>

<template>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" />
    <div>
        <h2>Listado de censos</h2>

        <button class="little-button" @click="changeSelectedVoting(New); changeEditing(true)">
            Nuevo censo
        </button>

        <div v-if="selectedVoting == New && editing == true">
            <p v-if="newCensusError != null" class="error">{{ newCensusError }}</p>
            <form @submit.prevent="saveCensus(newVotingId, newVoterId)">
                <label for="newVotingId">Id de la votación</label>
                <select required id="newVotingId" v-model="newVotingId">
                    <option v-for="voting in allVotings" :key="voting" :value="voting.id"> {{ voting.id }}. {{ voting.name}} </option>
                </select>
                <div>
                    <label for="filter"> Filtrar por: </label>
                    <select id="filter" v-model="filter" @change="valuesForFilter">
                        <option value=""> Ninguno </option>
                        <option v-for="filterType in filterTypes" :key="filterType" :value="filterType"> {{ parseFilter(filterType) }}</option>
                    </select>
                    <select v-if="filter=='religion' || filter=='gender' || filter=='civil_state' || filter=='works'" id="filterValue" v-model="filterValue" @change="applyFilter">
                        <option value=""> Ninguno </option>
                        <option v-for="filterValue in filterValues" :key="filterValue" :value="filterValue"> {{parseFilterValue(filterValue) }} </option>
                    </select>
                    <input type="text" v-if="filter=='country'" id="filterValue" v-model="filterValue" @change="applyFilter" :placeholder="'País...'">
                    <input type="number" v-if="filter=='born_year'" id="filterValue" v-model="filterValue" @change="applyFilter" :placeholder="'Año de nacimiento...'">
                </div>
                <label for="newVoterId">Añadir usuario</label>
                <select required id="newVoterId" v-model="newVoterId">
                    <option v-for="user in usersSubList" :key="user.id" :value="user.id"> {{ user.id }}. {{ user.username }}
                    </option>
                </select>
                <button class="little-button" type="submit">Añadir</button>
            </form>
        </div>

        <ul>
            <li v-for="voting in votings" :key="voting">
                <h3>
                    <button @click="changeSelectedVoting(voting)">
                        Voting: {{ voting }}
                    </button>
                </h3>
                <ul>
                    <li v-if="voting == selectedVoting">
                        {{ newCensusError }}
                        <form @submit.prevent="saveCensus">
                            <label for="newVoterId">Añadir usuario</label>
                            <select required id="newVoterId" v-model="newVoterId">
                                <option v-for="user in users" :key="user.id" :value="user.id"> {{ user.id }}. {{
                                    user.username }} </option>
                            </select>
                            <button class="little-button" type="submit">Añadir</button>
                        </form>
                        <div v-for="census in censusSubList" :key="census.id">
                            <div class="user_container">
                                <button class="user_container_element no_pointer_button">
                                    Id: {{ census.id }} - User: {{ census.voter_id }}
                                </button>
                                <button class="delete-census" @click="deleteCensus(census)">
                                    <i class="fa fa-trash" aria-hidden="true"></i>
                                </button>
                            </div>
                            <div class="waiting_container" v-if="waiting == census.voter_id">
                                <i class="fa fa-spinner fa-spin"></i>
                            </div>
                        </div>
                    </li>
                </ul>
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

.delete-census {
    width: auto;
    display: inline-block;
    margin-left: 10px;
    width: 20%;
    background-color: rgb(211, 91, 91);
}

ul li div>button {
    list-style-type: square;
    background-color: rgb(1, 88, 88);
}

.no_pointer_button:hover {
    cursor: default;
}

ul li form>select {
    list-style-type: square;
    margin-bottom: 5px;
}

ul li form>button {
    list-style-type: square;
    margin-bottom: 20px;
}

.user_container {
    display: flex
}

.user_container_element {
    display: inline-block
}

ul>li {
    margin-bottom: 0px;
}

.waiting_container {
    margin-top: 0;
    margin-bottom: 15px;
}</style>