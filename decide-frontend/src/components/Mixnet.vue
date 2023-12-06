<script>
import { ref, onMounted } from "vue";
import {MixnetForm,Auth} from "../../models/MixnetForm.js";

export default {
    setup() {

        const mixnets = ref([]);
        const votings = ref([]);
        const auths = ref([]);
        const selectedMixnet = ref(null);
        const newMixnet= ref(new MixnetForm())
        const newAuths= ref([]);
        const newAuth= ref(new Auth());
        const editing= ref(false);
        const New = ref("New");
        const newSelectedAuth = ref(null);

        const fetchMixnets = async () => {
            const response = await fetch("http://localhost:8000/mixnet", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
            });
            const data = await response.json();
            mixnets.value = data;
        };

        const fetchVotings = async () => {
        try {
            const response = await fetch("http://localhost:8000/voting/");
            const data = await response.json();
            votings.value = data;
        } catch (error) {
            console.error("Error:", error);
        }
    };

    const fetchAuths = async () => {
        try{
          const authResponse = await fetch(
            "http://localhost:8000/voting/all-auths/",
            {
              method: "GET",
              credentials: "include",
            }
          );
          const authData = await authResponse.json();
          auths.value = authData;
        } catch (error) {
            console.error("Error:", error);
            }
        };

        const saveMixnet= async () => {
            newAuths.array.forEach(auth => {
                newMixnet.value.auths.push(new Auth(auth));
            }); 

            const response = await fetch("http://localhost:8000/mixnet", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include",
                body: JSON.stringify(newMixnet),
            });
            const data = await response.json();
            mixnets.value.push(data);
            newMixnet.value = new MixnetForm();
            newAuths.value = [];
            newAuth.value = new Auth();
        };

        const addNewAuth = () => {
            newAuths.value.push(newAuth);
            newAuth.value = new Auth();
        };

        const addNewSelectedAuth = () => {
            const auth = auths.value.find((a) => a.id === newSelectedAuth.value);
            newAuths.value.push(auth);
            auths.value = auths.value.filter((a) => a !== auth);
            newSelectedAuth.value = null;
        };

        const removeAuth = (auth) => {
            newAuths.value = newAuths.value.filter((a) => a !== auth);
            auths.value.push(auth);
        };

        const changeEditing= (value) => {
            editing.value = value;
            newMixnet.value = new MixnetForm();
            newAuths.value = [];
            newAuth.value = new Auth();
            newSelectedAuth.value = null;
        };

        const changeSelected =async (mixnet) => {
            if (mixnet == "New") {
                await fetchAuths();
                await fetchVotings();
            }
            selectedMixnet.value = selectedMixnet.value === mixnet ? null : mixnet;
        };

        onMounted(()=>{
            fetchMixnets();
            }
        );

        return{
            mixnets,
            selectedMixnet,
            newMixnet,
            newAuths,
            newAuth,
            editing,
            New,
            newSelectedAuth,
            auths,
            votings,
            saveMixnet,
            addNewAuth,
            removeAuth,
            changeEditing,
            fetchMixnets,
            changeSelected,
            addNewSelectedAuth,
        }
    }
}
</script>

<template>
  <div>
    <h2>Listado de Mixnets</h2>
    <ul>
        <li>
        <button class="little-button" @click="changeSelected(New); changeEditing(true)">
          Nueva Mixnet
        </button>

        <div v-if="selectedMixnet == New && editing == true">
          <div>
            <form @submit.prevent="saveMixnet">
              <label for="votacion">Votación: </label>
              <select id="votacion" v-model="newMixnet.voting_id">
                <option v-for="voting in votings" :key="voting.id" :value="voting.id">
                  {{ voting.name }}
                </option>
              </select>
              <p>--AUTHS--</p>
              <table>
                <tr>
                <th>Nombre de la auth</th>
                <th>URL</th>
                <th></th>
                </tr>
                <tr v-for="auth in newAuths">
                <td>{{ auth.name }}</td>
                <td>{{ auth.url }}</td>
                <td><button class="little-button" @click="removeAuth(auth)">Eliminar</button></td>
                </tr>
                </table>
                
              <p>Añadir Auth existente</p>
              <select id="auth" v-model="newSelectedAuth">
                <option v-for="auth in auths" :key="auth.id" :value="auth.id">
                  {{ auth.name }}
                </option>
            </select>
            <button type="button" class="little-button button-inline" @click="addNewSelectedAuth">
                Añadir
            </button>
            <p>O</p>
              <p>Crear nueva Auth</p>
              <label for="name">Nombre: </label>
              <input type="text" id="name" v-model="newAuth.name" />
              <label for="url">Opción: </label>
              <input type="text" id="url" v-model="newAuth.url" />
              <button type="button" class="little-button button-inline" @click="addNewAuth">
                Añadir
              </button>
              <p>--Pubkey--</p>
              <br>
              <button class="little-button" @click="changeEditing(false)">
                Cancelar
              </button>
              <button class="little-button" :disabled="newAuths.length==0" :class="{'little-button':true, 'disabled':newAuths.length==0}" type="submit">
                Guardar
              </button>
            </form>
          </div>
        </div>
      </li>
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
