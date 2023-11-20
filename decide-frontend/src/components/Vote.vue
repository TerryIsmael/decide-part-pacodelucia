<script>
import { ref, onMounted } from "vue";
import Vote from "../../models/Vote.js";

export default {
    setup() {
        const votes = ref({});
        const selectedVote = ref(null);
        const New = ref("New");
        const editing = ref(false);
        const votings = ref([]);
        const users = ref([]);
        const newVote = ref(new Vote());
        const loading = ref(false);

        const fetchvotes = async () => {
        try {
            const response = await fetch("http://localhost:8000/store/", {
                method: "GET",
                credentials: "include",
            }
                );
            const data = await response.json();
            data.map((vote) => {
                vote.a = BigInt(vote.a);
                vote.b = BigInt(vote.b);
            });
            votes.value = data;
        } catch (error) {
            console.error("Error:", error);
        }
        };

        const changeSelected = (id) => {
            selectedVote.value = selectedVote.value === id ? null : id;
        };


        onMounted(()=>{
            fetchvotes();
            }
            );

        return {
            votes,
            selectedVote,
            New,
            editing,
            votings,
            users,
            newVote,
            loading,
            fetchvotes,
            changeSelected,
        };
    },
};
</script>


<template>
  <div>
    <h2>Listado de votos</h2>
    <ul>
        <li v-for="vote in votes" :key="vote.id">
            <h3>
                <button @click="changeSelected(vote.id);">
                    {{ vote.voting_id }}:{{  vote.voter_id }}
                </button>

                <div v-if="selectedVote == vote.id">
                    <div>
                        <p><span class="bold">Id:</span> {{ vote.id }}</p>
                        <p><span class="bold">Voting id:</span> {{ vote.voting_id }}</p>
                        <p><span class="bold">Voter id:</span> {{ vote.voter_id }}</p>
                        <p><span class="bold">A:</span> {{ vote.a }}</p>
                        <p><span class="bold">B:</span> {{ vote.b }}</p>
                    </div>
                </div>
            </h3>
        </li>
    </ul>
</div>

</template>


<style scoped>

.big-n{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    align-items: center;
}
.big-n > input{
    height: 30px;
    margin-bottom: 20px;
    padding: 5px;
    border-radius: 5px;
    border: 2px solid grey;
    width: 300%;
}
</style>