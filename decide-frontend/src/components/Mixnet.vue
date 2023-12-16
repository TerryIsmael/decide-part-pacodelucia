<script>
import { ref, onMounted, inject } from "vue";

export default {
    setup() {
        const logged = inject("logged");
        const navBarLoaded = inject('navBarLoaded')

        const init = async () => {
            while (!navBarLoaded.value) {
                await new Promise(resolve => setTimeout(resolve, 100));
            }
            navBarLoaded.value = false;
            if (logged.value) {
                //Init functions
                fetchMixnets();
            }
        }

        onMounted(init);

        const mixnets = ref([])
        const selectedMixnet = ref(null);

        const fetchMixnets = async () => {
            const response = await fetch(import.meta.env.VITE_API_URL + "/mixnet", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });
            const data = await response.json();
            mixnets.value = data;
        };

        const changeSelected =async (mixnet) => {
            if (mixnet == "New") {
                await fetchAuths();
                await fetchVotings();
            }
            selectedMixnet.value = selectedMixnet.value === mixnet ? null : mixnet;
        };

        return {
            mixnets,
            selectedMixnet,
            fetchMixnets,
            changeSelected,
        }
    }
}
</script>

<template>
  <div>
    <h2>Listado de Mixnets</h2>
    <ul>
      <li class="big-container" v-for="mixnet in mixnets" :key="mixnet.id">
        <h3>
          <button @click="changeSelected(mixnet)">
            Voting {{ mixnet.voting_id }}
          </button>
        </h3>
        <div v-if="mixnet == selectedMixnet" :key="mixnet.id">
          <p><span class="bold">Id:</span> {{ mixnet.id }}</p>
          <p><span class="bold">Voting:</span> {{ mixnet.voting_id }}</p>
          <p><span class="bold">--Auths--</span></p>
          <table>
            <tr>
              <th>Nombre de la auth</th>
              <th>URL</th>
              <th>Yo</th>
            </tr>
            <tr v-for="auth in mixnet.auths">
              <td>{{ auth.name }}</td>
              <td>{{ auth.url }}</td>
              <td>{{ auth.me }}</td>
            </tr>
          </table>
          <div v-if="mixnet.pubkey">
            <p><span class="bold">--Pubkey--</span></p>
            <p><span class="bold">P:</span> {{ mixnet.pubkey.p }}</p>
            <p><span class="bold">G:</span> {{ mixnet.pubkey.g }}</p>
            <p><span class="bold">Y:</span> {{ mixnet.pubkey.y }}</p>
        </div>
        <br>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>

.disabled{
    background-color: #cccccc;
    color: #666666;
    border-color: #cccccc;
}

</style>
