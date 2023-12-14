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
        const waiting = ref(null);
        
        const logged = inject("logged");
        const navBarLoaded = inject('navBarLoaded')

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
                    }else{
                        return a.voting_id - b.voting_id;}
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
            if (selectedVoting.value != null) {
                censusSubList.value = censuss.value.filter((census) => census.voting_id == selectedVoting.value);
            } else {
                selectedVoting.value = null;
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
            const censusJson ={
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

        return {
            censuss,
            votings,
            allVotings,
            censusSubList,
            New,
            editing,
            users,
            newCensus,
            newVoterId,
            newVotingId,
            newCensusError,
            selectedVoting,
            waiting,
            fetchCensuss,
            changeSelectedVoting,
            saveCensus,
            changeEditing,
            deleteCensus,
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
                    <option v-for="voting in allVotings" :key="voting" :value="voting.id"> {{ voting.id }} </option>
                </select>
                <label for="newVoterId">Añadir usuario</label>
                <select required id="newVoterId" v-model="newVoterId">
                    <option v-for="user in users" :key="user.id" :value="user.id"> {{ user.id }} </option>
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
                                <option v-for="user in users" :key="user.id" :value="user.id"> {{ user.id }} </option>
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
                            <div class="waiting_container" v-if="waiting==census.voter_id">
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
    display:inline-block;
    margin-left: 10px;
    width: 20%;
    background-color: rgb(211, 91, 91);
}

ul li div>button {
    list-style-type: square;
    background-color: rgb(1, 88, 88);
}

.no_pointer_button:hover {
    cursor:default;
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
    display:flex
}

.user_container_element {
    display:inline-block
}

ul >li {
    margin-bottom: 0px;
}

.waiting_container{
    margin-top: 0;
    margin-bottom: 15px;
}

</style>