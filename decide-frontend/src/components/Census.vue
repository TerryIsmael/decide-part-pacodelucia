<script>
import { ref, onMounted } from "vue";
import { Census } from "../../models/Census.js";

export default {
    setup() {
        const censuss = ref({});
        const selectedVoting = ref(null);
        const censusSubList = ref([]);
        const votings = ref([]);
        const New = ref("New");
        const editing = ref(false);
        const newCensus = ref(new Census());
        const newVoterId = ref("");
        const newVotingId = ref("");
        const newCensusError = ref(null);
        const users = ref([]);

        const fetchCensuss = async () => {
            try {
                const response = await fetch("http://localhost:8000/census/all-censuss/", {
                    method: "GET",
                    credentials: "include",
                });

                const data = await response.json();
                censuss.value = data;
                censuss.value.forEach((census) => {
                    votings.value = [...new Set([...votings.value, census.voting_id])];
                    votings.value = votings.value.sort((a, b) => {
                        return a - b;
                    });
                });
                const response2 = await fetch("http://localhost:8000/authentication/all-users/", {
                    method: "GET",
                    credentials: "include",
                });
                const data2 = await response2.json();
                users.value = data2;

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

            if (newVoterId.value === undefined || newVoterId.value.trim() === "" || newVotingId.value === undefined || newVotingId.value.trim() === "") {
                newCensusError.value = ("No se puede guardar un censo vacío");
                return;
            }
            else
                newCensusError.value = null;

            if (newOptionError.value != null)
                return;

            editing.value = false;

            const newCensus = {
                voting_id: newVotingId.value,
                voters: [newVoterId.value],
            };

            try {
                await fetch("http://localhost:8000/census/", {
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
            await fetchCensuss();
        };

        onMounted(fetchCensuss);

        return {
            censuss,
            votings,
            censusSubList,
            New,
            editing,
            users,
            newCensus,
            newVoterId,
            newVotingId,
            newCensusError,
            selectedVoting,
            fetchCensuss,
            changeSelectedVoting,
            saveCensus,
        };
    },
};
</script>

<template>
    <div>
        <h2>Listado de censos</h2>
        <ul>
            <li class="big-container" v-for="voting in votings" :key="voting">
                <h3>
                    <button @click="changeSelectedVoting(voting)">
                        Voting: {{ voting }}
                    </button>
                </h3>
                <ul>
                    <li v-if="voting == selectedVoting">
                        <form @submit.prevent="saveCensus(voting.id, newVoterId)">
                            <label for="newVoterId">Añadir usuario</label>
                            <select required id="newVoterId" v-model="newVoterId">
                                <option v-for="user in users" :key="user.id" :value="user"> {{ user.id }} </option>
                            </select>
                            <button class="little-button" type="submit">Añadir</button>
                        </form>
                        <div v-for="census in censusSubList" :key="census.id">
                            <button>
                                Id: {{ census.id }} - User: {{ census.voter_id }}
                            </button>
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

ul li div>button {
    margin-left: 20px;
    list-style-type: square;
    background-color: rgb(1, 88, 88);
}
</style>