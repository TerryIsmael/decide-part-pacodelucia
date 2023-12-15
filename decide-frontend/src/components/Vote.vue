<script>
import { ref, onMounted, inject } from "vue";
import Vote from "../../models/Vote.js";

export default {
    setup() {
        const votes = ref([]);
        const selectedVote = ref(null);
        const selectedVoting = ref(null);
        const editing = ref(false);
        const votings = ref([]);
        const users = ref([]);
        const newVote = ref(new Vote());
        const votingVotes = ref([]);
        const votesSubList = ref([]);
        const navBarLoaded = inject("navBarLoaded");
        const logged = inject("logged");

        const init = async () => {
            while (!navBarLoaded.value) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            navBarLoaded.value = false;
            if (logged.value) {
                //Init functions
                fetchvotes();
            }
        }

        onMounted(init);
        const fetchvotes = async () => {
            try {
                const response = await fetch(import.meta.env.VITE_API_URL + "/store/front/", {
                    method: "GET",
                    credentials: "include",
                }
                );
                const data = await response.json();
                await data.map((vote) => {
                    vote.a = BigInt(vote.a);
                    vote.b = BigInt(vote.b);
                });
                votes.value = data;
                const set = new Set();
                votes.value.forEach((vote) => set.add(vote.voting_id));
                votingVotes.value = [...set].sort((a, b) => a - b);
                if (selectedVoting.value != null) {
                    votesSubList.value = votes.value.filter((vote) => vote.voting_id == selectedVoting.value);
                }
            } catch (error) {
                console.error("Error:", error);
            }
        };

        const changeSelectedVote = (id) => {
            selectedVote.value = selectedVote.value === id ? null : id;
        };

        const changeSelectedVoting = (id) => {
            selectedVoting.value = selectedVoting.value === id ? null : id;
            if (selectedVoting.value != null) {
                votesSubList.value = votes.value.filter((vote) => vote.voting_id == selectedVoting.value);
            } else {
                selectedVote.value = null;
            }
        };

        const deleteVote = async (id) => {
            const json = {
                "id": id
            }
            await fetch(import.meta.env.VITE_API_URL + "/store/front/", {
                method: "DELETE",
                credentials: "include",
                body: JSON.stringify(json),
                headers: {
                    "Content-Type": "application/json",
                },
            });
            await fetchvotes();
        };

        return {
            votes,
            selectedVote,
            selectedVoting,
            editing,
            votings,
            users,
            newVote,
            fetchvotes,
            changeSelectedVote,
            changeSelectedVoting,
            deleteVote,
            votingVotes,
            votesSubList,
        };
    },
};
</script>

<template>
    <div>
        <h2>Listado de votos</h2>
        <ul>
            <li class="big-container" v-for="votingVote in votingVotes" :key="votingVote">

                <button @click="changeSelectedVoting(votingVote)">
                    Voting: {{ votingVote }}
                </button>
                <ul>
                    <li v-if="votingVote == selectedVoting" v-for="vote in votesSubList" :key="vote.id">
                        <button @click="changeSelectedVote(vote.id)">
                            User: {{ vote.voter_id }}
                        </button>

                        <div v-if="selectedVote == vote.id">
                            <div>
                                <p><span class="bold">Id:</span> {{ vote.id }}</p>
                                <p><span class="bold">Voting id:</span> {{ vote.voting_id }}</p>
                                <p><span class="bold">Voter id:</span> {{ vote.voter_id }}</p>
                                <p><span class="bold">A:</span> {{ vote.a }}</p>
                                <p><span class="bold">B:</span> {{ vote.b }}</p>
                                <button class="little-button" style="background-color: rgb(211, 91, 91);" @click="deleteVote(vote.id)">Eliminar</button>
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
    margin-bottom: 10px;
}

.little-button {
    width: auto;
}

ul ul li > button {
    list-style-type: square;
    background-color: rgb(1, 88, 88);
    margin-bottom: 10px;
}
</style>