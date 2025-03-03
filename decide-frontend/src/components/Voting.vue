<script>
import { ref, onMounted, inject } from "vue";
import Voting from "../../models/Voting.js";

export default {
  setup() {
    const votings = ref({});
    const selectedVoting = ref(null);
    const New = ref("New");
    const editing = ref(false);
    const questions = ref([]);
    const auths = ref([]);
    const newVoting = ref(new Voting());
    const loading = ref(false);
    const errorMessage = ref("");

    const fetchVotings = async () => {
      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/voting/");
        const data = await response.json();
        votings.value = data;
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const fetchQuestions = async () => {
      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/voting/all-questions/", {
          method: "GET",
          credentials: "include",
        });
        const data = await response.json();
        questions.value = data;
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const fetchAuths = async () => {
      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/base/auth/", {
          method: "GET",
          credentials: "include",
        });
        const data = await response.json();
        auths.value = data;
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const changeEditing = async (newValue) => {
      errorMessage.value = "";
      if (newValue == true) {
        if (selectedVoting != "New") {
          newVoting.value = { ...votings.value.find((voting) => voting.id === selectedVoting.value) };
        }
        try {
          const questionResponse = await fetch(
            import.meta.env.VITE_API_URL + "/voting/all-questions/",
            {
              method: "GET",
              credentials: "include",
            }
          );

          const questionData = await questionResponse.json();
          questions.value = questionData;
          const authResponse = await fetch(
            import.meta.env.VITE_API_URL + "/base/auth/",
            {
              method: "GET",
              credentials: "include",
            }
          );

          const authData = await authResponse.json();
          auths.value = authData;

          if (questionResponse.ok && authResponse.ok) {
            editing.value = newValue;
          } else {
            alert("Se produjo un error al cargar los datos");
          }
        } catch (error) {
          console.error("Error:", error);
        }
      } else {
        editing.value = newValue;
      }
    };

    const applyAction = async (votingId, action) => {
      loading.value = true;
      const votingAccion = {
        id: votingId,
        action: action,
      };
      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/voting/voting/",
          {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(votingAccion),
          }
        );
      } catch (error) {
        console.error("Error:", response.status, error.json());
      }
      fetchVotings();
      loading.value = false;
    };

    const deleteVoting = async (id) => {
      const votingDelete = {
        id: id,
      };
      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/voting/voting/",
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(votingDelete),
          }
        );
      } catch (error) {
        console.error("Error:", response.status, error.json());
      }
      fetchVotings();
    }

    const saveVoting = async () => {
      if (newVoting.value.name.trim() === "" || newVoting.value.name == undefined || newVoting.value.desc.trim() === "" || newVoting.value.desc == undefined) {
        errorMessage.value = "El nombre y la descripción no pueden estar vacíos";
        return;
      }
      const votingPost = {
        id: newVoting.value.id,
        name: newVoting.value.name,
        desc: newVoting.value.desc,
        question: newVoting.value.question.id,
        auths: newVoting.value.auths.map((auth) => auth.id),
      };

      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/voting/voting/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
          body: JSON.stringify(votingPost),
        });
        newVoting.value = new Voting();
        errorMessage.value = "";
        editing.value = false;
      } catch (error) {
        console.error("Error:", response.status, error.json());
      }

      newVoting.value = new Voting();
      fetchVotings();
    };

    const isNumberInTally = (voting, number) => {
      return voting.tally.includes(number);
    };

    const showForm = (voting) => {
      selectedVoting.value = voting;
    };

    const changeSelected = (id) => {
      selectedVoting.value = selectedVoting.value === id ? null : id;
      errorMessage.value = "";
    };

    const dateFormat = (oldDate) => {
      if (oldDate == null) {
        return null;
      }
      const date = new Date(oldDate);

      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();
      const hours = date.getHours();
      const minutes = date.getMinutes();

      const formattedDay = day < 10 ? `0${day}` : day;
      const formattedMonth = month < 10 ? `0${month}` : month;
      const formattedHours = hours < 10 ? `0${hours}` : hours;
      const formattedMinutes = minutes < 10 ? `0${hours}` : minutes;

      return `${formattedDay}/${formattedMonth}/${year} ${formattedHours}:${formattedMinutes}`;
    };

    onMounted(fetchVotings);

    const transformBigInt = (bigIntValue) => {

      const chunkSize = 10;
      const chunks = [];

      for (let i = 0; i < bigIntValue.length; i += chunkSize) {
        console.log(bigIntValue.slice(i, i + chunkSize));
        chunks.push(bigIntValue.slice(i, i + chunkSize));
      }

      const transformedNumber = chunks.join("");
      return transformedNumber;
    }

    return {
      votings,
      selectedVoting,
      New,
      editing,
      questions,
      auths,
      newVoting,
      loading,
      errorMessage,
      showForm,
      changeSelected,
      dateFormat,
      isNumberInTally,
      changeEditing,
      saveVoting,
      applyAction,
      deleteVoting,
      fetchQuestions,
      fetchAuths,
      transformBigInt,
    };
  },
};
</script>

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    integrity="nueva-cadena-de-integridad" crossorigin="anonymous">
  <div class="principal_div">
    <h2>Listado de votaciones</h2>
    <ul>
      <button class="little-button" @click="changeSelected(New), changeEditing(true)"> Nueva votación </button>

      <div v-if="selectedVoting == 'New' && editing == true">
        <form @submit.prevent="saveVoting(newVoting)">
          <div>
            <p class="bold" style="color:rgb(211, 91, 91)">{{ errorMessage }}</p>
          </div>
          <div>
            <label for="name">Nombre: </label>
            <input type="text" id="name" v-model="newVoting.name" required />
          </div>
          <div>
            <label for="desc">Descripción: </label>
            <textarea required id="desc" rows="10" columns="90" v-model="newVoting.desc"></textarea>
          </div>
          <div>
            <label for="question">Pregunta: </label>
            <select required id="question" v-model="newVoting.question">
              <option v-for="question in questions" :key="question.id" :value="question"> {{ question.desc }} </option>
            </select>
            <button class="little-button adjusted" type="button" onclick="window.open('/admin/question', '_blank')"> Nueva...</button>
            <button class="little-button adjusted" type="button" @click="fetchQuestions"><i class="fas fa-sync-alt"></i></button>
          </div>
          <label for="auths">Auths: </label>
          <div style="display:flex; align-items: center;justify-content: center;">
            <select style="height: 60%;" required id="auths" v-model="newVoting.auths" multiple>
              <option v-for="auth in auths" :key="auth.id" :value="auth"> {{ auth.name }} </option>
            </select>
            <button class="little-button auth_adjusted" type="button" onclick="window.open('/admin/auth', '_blank')"> Nueva...</button>
            <button class="little-button auth_adjusted" type="button" @click="fetchAuths"><i class="fas fa-sync-alt"></i></button>
          </div>
          <div>
            <button class="little-button" @click="changeEditing(false)"> Cancelar </button>
            <button type="submit" class="little-button">Crear</button>
          </div>
        </form>
      </div>

      <li v-for="voting in votings" :key="voting.id">
        <h3>
          <button @click="changeSelected(voting.id); changeEditing(false);">
            {{ voting.name }}
            <span v-if="voting.start_date != null"> - </span>
            {{ dateFormat(voting.start_date) }}
            <span v-if="voting.end_date != null"> - </span>
            {{ dateFormat(voting.end_date) }}
          </button>
        </h3>

        <div v-if="selectedVoting === voting.id">
          <div v-if="!editing">
            <button :disabled="loading" v-if="voting.start_date == null" class="little-button"
              @click="applyAction(voting.id, 'start')"> Empezar </button>
            <button :disabled="loading" v-if="voting.start_date != null && voting.end_date == null" class="little-button"
              @click="applyAction(voting.id, 'stop')"> Parar </button>
            <button :disabled="loading" v-if="voting.end_date != null && voting.postproc == null" class="little-button"
              @click="applyAction(voting.id, 'tally')"> Recuento </button>
            <p class="bold" v-if="loading">Cargando...</p>

            <p><span class="bold">Id:</span> {{ voting.id }}</p>
            <p><span class="bold">Descripción: </span>{{ voting.desc }}</p>
            <p>
              <span class="bold">Pregunta: </span> {{ voting.question.desc }}
            </p>
            <p>
              <span class="bold">Opción ganadora: </span>
              {{ voting.tally ? voting.tally.toString() : "No hay recuento" }}
            </p>
            <h4 v-if="voting.postproc == null">No finalizada</h4>
            <table v-if="voting.postproc == null">
              <tr>
                <th>Número opción</th>
                <th>Opción</th>
              </tr>

              <tr v-for="option in voting.question.options">
                <td>{{ option.number }}</td>
                <td>{{ option.option }}</td>
              </tr>
            </table>

            <table v-else>
              <tr>
                <th>Número opción</th>
                <th>Opción</th>
                <th>Votos</th>
              </tr>
              <tbody>
                <tr v-for="option in voting.postproc" :key="option.number"
                  :class="{ remarkable: isNumberInTally(voting, option.number), }">
                  <td>{{ option.number }}</td>
                  <td>{{ option.option }}</td>
                  <td>{{ option.votes }}</td>
                </tr>
              </tbody>
            </table>
            <table>
              <tr>
                <th>Nombre de la auth</th>
                <th>URL</th>
                <th>Yo</th>
              </tr>
              <tr v-for="auth in voting.auths">
                <td>{{ auth.name }}</td>
                <td>{{ auth.url }}</td>
                <td>{{ auth.me }}</td>
              </tr>
            </table>
            <button v-if="voting.start_date == null" class="little-button" @click="changeEditing(true)"> Editar </button>
            <button class="little-button deleteButton" @click="deleteVoting(voting.id)"> Eliminar </button>
          </div>
          <div v-else>
            <form @submit.prevent="saveVoting">

              <div>
                <p class="bold" style="color:rgb(211, 91, 91)">{{ errorMessage }}</p>
              </div>
              <div>
                <label for="name">Nombre: </label>
                <input type="text" id="name" v-model="newVoting.name" required />
              </div>
              <div>
                <label for="desc">Descripción: </label>
                <textarea id="desc" rows="10" columns="90" v-model="newVoting.desc" required></textarea>
              </div>
              <div>
                <label for="question">Pregunta: </label>
                <select id="question" v-model="newVoting.question">
                  <option v-for="question in questions" :key="question.id" :value="question">
                    {{ question.desc }}
                  </option>
                </select>
                <button class="little-button adjusted" type="button" onclick="window.open('/admin/question', '_blank')">
                  Nueva...</button>
                <button class="little-button adjusted" type="button" @click="fetchQuestions"><i class="fas fa-sync-alt"></i></button>
              </div>
              <label for="auths">Auths: </label>
              <div style="display:flex; align-items: center;justify-content: center;">
                <select style="height: 60%;" id="auths" v-model="newVoting.auths" multiple>
                  <option v-for="auth in auths" :key="auth.id" :value="auth">
                    {{ auth.name }}
                  </option>
                </select>
                <button class="little-button auth_adjusted" type="button" onclick="window.open('/admin/auth', '_blank')">
                  Nueva...</button>
                <button class="little-button auth_adjusted" type="button" @click="fetchAuths"><i class="fas fa-sync-alt"></i></button>
              </div>
              <div v-if="editing">
                <button class="little-button" @click="changeEditing(false)"> Cancelar </button>
                <button class="little-button" type="submit"> Guardar </button>
              </div>
            </form>
            </div>
            <p v-if="voting.start_date != null">
              <span class="bold">Fecha de inicio: </span>
              {{ dateFormat(voting.start_date) }}
            </p>
            <p v-if="voting.end_date != null">
              <span class="bold">Fecha de fin: </span>
              {{ dateFormat(voting.end_date) }}
            </p>
            <div v-if="voting.start_date != null">
              <h4>- PUB_KEY -</h4>

              <p><span class="bold">P:</span> {{ BigInt.fromBigInt(voting.pub_key.p) }}</p>
              <p><span class="bold">G:</span> {{ BigInt.fromBigInt(voting.pub_key.g) }}</p>
              <p><span class="bold">Y:</span> {{ BigInt.fromBigInt(voting.pub_key.y) }}</p>
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
}

button:disabled {
  background-color: grey;
}

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
}

button:disabled {
  background-color: grey;
}

.adjusted {
  width: auto;
}

.auth_adjusted {
  width: auto;
  height: 30%;
}

.big_auth {
  height: 60%;
}
</style>