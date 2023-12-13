<script>
import { ref, onMounted } from "vue";
import {MixnetForm,Auth} from "../../models/MixnetForm.js";
import {useRouter} from "vue-router";

export default {
    setup() {
        const token = ref('');
        const router = useRouter();

        const init = () => {
            var cookies = document.cookie.split(';');
            cookies.forEach(cookie => {
                var cookiePair = cookie.split('=');
                if (cookiePair[0].trim() === 'sessionid' && cookiePair[1]) {
                    token = pair[1];
                    fetchMixnets();
                }
            });

        }

        const mixnets = ref([])
        const selectedMixnet = ref(null);

        const isUserLogged = async () => {
            fetch(import.meta.env.VITE_API_URL + '/authentication/admin-auth/', {
                    method: 'GET',
                    credentials: 'include',
                })
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        router.push('/admin/login');
                    }
                })
                .then((data) => {
                    if (data.user_data && data.user_data.is_staff) {
                        
                    } else {
                        router.push('/admin/login');
                    }
                })
                .catch(() => {
                    router.push('/admin/login');
                });
        }

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

        onMounted(()=>{
            init();
            isUserLogged();
            fetchMixnets();
            }
        );

        return{
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
            <p><span class="bold">P:</span> {{ BigInt(mixnet.pubkey.p) }}</p>
            <p><span class="bold">G:</span> {{ BigInt(mixnet.pubkey.g) }}</p>
            <p><span class="bold">Y:</span> {{ BigInt(mixnet.pubkey.y) }}</p>
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
