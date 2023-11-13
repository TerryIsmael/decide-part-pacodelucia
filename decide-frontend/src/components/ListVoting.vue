<script>
import { ref, onMounted } from 'vue';
import Voting from '../../models/Voting.js';

//TODO: Cambiar estado de votacion, cambiar preguntas y auths (redireccionar) y conseguir el post

export default {

  setup() {
    const votaciones = ref({});
    const votacionSeleccionada = ref(null);
    const New = ref("New");
    const editing = ref(false);
    const questions = ref([]);
    const auths = ref([]);
    const newVoting = ref(new Voting());
    const fetchVotaciones = async () => {
      try {
        const response = await fetch('http://localhost:8000/voting/');
        const data = await response.json();
        votaciones.value = data;
      } catch (error) {
        console.error('Error:', error);
      }
    };

    const changeEditing = async (newValue) => {
      if (newValue == true) {
        try {
          const questionResponse = await fetch('http://localhost:8000/voting/all-questions/', {
            method: 'GET',
            credentials: 'include'
          });

          const questionData = await questionResponse.json();
          questions.value = questionData;
          const authResponse = await fetch('http://localhost:8000/voting/all-auths/', {
            method: 'GET',
            credentials: 'include'
          });

          const authData = await authResponse.json();
          auths.value = authData;

          if (questionResponse.ok && authResponse.ok) {
            editing.value = newValue;
          } else {
            alert("Se produjo un error al cargar los datos");
          }
        } catch (error) {
          console.error('Error:', error);
        }
      } else {
        editing.value = newValue;
      }
    };

    const guardarVotacion = (votacion) => {
      pass
    };

    const isNumberInTally = (votacion, number) => {
      return votacion.tally.includes(number);
    };

    const mostrarFormulario = (votacion) => {
      votacionSeleccionada.value = votacion;
    };

    const agregarVotacion = (nuevaVotacion) => {
      if (nuevaVotacion.id) {
        const index = votaciones.value.findIndex(v => v.id === nuevaVotacion.id);
        if (index !== -1) {
          votaciones.value.splice(index, 1, nuevaVotacion);
        }
      } else {
        nuevaVotacion.id = votaciones.value.length + 1;
        votaciones.value.push(nuevaVotacion);
      }
      votacionSeleccionada.value = null;
    };

    const cambiarSeleccionada = (id) => {
      votacionSeleccionada.value = votacionSeleccionada.value === id ? null : id;
    };

    const formatearFecha = (fecha_original) => {
      if (fecha_original == null) {
        return null;
      }
      const fecha = new Date(fecha_original);

      const dia = fecha.getDate();
      const mes = fecha.getMonth() + 1; // Los meses comienzan desde 0
      const anio = fecha.getFullYear();
      const horas = fecha.getHours();
      const minutos = fecha.getMinutes();

      const diaFormateado = (dia < 10) ? `0${dia}` : dia;
      const mesFormateado = (mes < 10) ? `0${mes}` : mes;
      const horasFormateadas = (horas < 10) ? `0${horas}` : horas;
      const minutosFormateados = (minutos < 10) ? `0${minutos}` : minutos;

      const fechaFormateada = `${diaFormateado}/${mesFormateado}/${anio} ${horasFormateadas}:${minutosFormateados}`;

      return fechaFormateada;
    };

    onMounted(fetchVotaciones);
    
    return {
      votaciones,
      votacionSeleccionada,
      mostrarFormulario,
      agregarVotacion,
      cambiarSeleccionada,
      formatearFecha,
      isNumberInTally,
      New,
      editing,
      questions,
      auths,
      changeEditing,
      newVoting,
    };
  },
};
</script>

<template>
  <div>
    <h2>Listado de Votaciones</h2>
    <ul>
      <li v-for="votacion in votaciones" :key="votacion.id">

        <h3>
          <button @click="cambiarSeleccionada(votacion.id); changeEditing(false)">
          {{ votacion.name }} <span v-if="votacion.start_date!=null"> - </span> {{ formatearFecha(votacion.start_date)}} <span v-if="votacion.end_date!=null"> - </span> {{ formatearFecha(votacion.end_date) }}</button>
        </h3>

        <div v-if="votacionSeleccionada === votacion.id">
          <p> <span class="bold">Id:</span> {{ votacion.id }} </p>
          <div v-if="!editing">
            <p> <span class="bold">Descripción: </span>{{ votacion.desc }} </p>
            <p> <span class="bold">Pregunta: </span> {{ votacion.question.desc }} </p>
            <p> <span class="bold">Opción ganadora: </span> {{ votacion.tally ? votacion.tally.toString() : 'No hay recuento' }}</p>
            
            <table v-if="votacion.postproc == null">
              <tr>
                <th> Número opción </th>
                <th> Opción </th>
              </tr>

              <tr v-for="option in votacion.question.options">
                <td> {{ option.option }} </td>
                <td> {{ option.number }} </td>
              </tr>
            </table>

            <table v-else>
              <tr>
                <th> Número opción </th>
                <th> Opción </th>
                <th> Votos </th>
              </tr>
              <tbody>
                <tr v-for="option in votacion.postproc" :key="option.number"
                  :class="{ 'remarkable': isNumberInTally(votacion, option.number) }">
                  <td>{{ option.number }}</td>
                  <td>{{ option.option }}</td>
                  <td>{{ option.votes }}</td>
                </tr>
              </tbody>
            </table>

            <table>
              <tr>
                <th> Nombre de la auth </th>
                <th> URL </th>
                <th> Yo </th>
              </tr>
              <tr v-for="auth in votacion.auths">
                <td> {{ auth.name }} </td>
                <td> {{ auth.url }} </td>
                <td> {{ auth.me }} </td>
              </tr>
            </table>
          </div>

          <div v-else>
            <div>
              <label for="name">Nombre: </label>
              <input type="text" id="name" v-model="votacion.name" />
            </div>
            <div>
              <label for="desc">Descripción: </label>
              <textarea id="desc" rows=10 columns="90" v-model="votacion.desc"></textarea>
            </div>
            <div>
              <label for="question">Pregunta: </label>
              <select id="question" v-model="votacion.question">
                <option v-for="question in questions" :key="question.id" :value="question">
                  {{ question.desc }}
                </option>
              </select>
            </div>
            <div>
              <label for="auths">Auths: </label>
              <select id="auths" v-model="votacion.auths" multiple>
                <option v-for="auth in auths" :key="auth.id" :value="auth">
                  {{ auth.name }}
                </option>
              </select>
            </div>
          </div>

          <p v-if="votacion.start_date != null"><span class="bold">Fecha de inicio: </span> {{ formatearFecha(votacion.start_date) }} </p>
          <p v-if="votacion.end_date != null"><span class="bold">Fecha de fin: </span> {{ formatearFecha(votacion.end_date) }} </p>
          <h4 v-if="votacion.postproc == null">No finalizada</h4>
          <div v-if="votacion.start_date != null">
            <h4>- PUB_KEY -</h4>
            <p> <span class="bold">P:</span> {{ BigInt(votacion.pub_key.p) }} </p>
            <p> <span class="bold">G:</span> {{ BigInt(votacion.pub_key.g) }} </p>
            <p> <span class="bold">Y:</span> {{ BigInt(votacion.pub_key.y) }} </p>
          </div>

          <div v-if="!editing">
            <button class="little-button" @click="changeEditing(true)">Comenzar a editar</button>
          </div>
          <div v-else>
            <button class="little-button" @click="changeEditing(false)">Cancelar</button>
            <button class="little-button" @click="guardarVotacion(votacion)">Guardar</button>
          </div>
        </div>
      </li>
    </ul>

    <button class="little-button" @click="cambiarSeleccionada(New), changeEditing(true)">Crear Nueva Votación</button>

    <br><br>
    <div v-if="votacionSeleccionada == 'New' && editing == true">
      <div>
        <label for="name">Nombre: </label>
        <input type="text" id="name" v-model="newVoting.name" />
      </div>
      <div>
        <label for="desc">Descripción: </label>
        <textarea id="desc" rows=10 columns="90" v-model="newVoting.desc"></textarea>
      </div>
      <div>
        <label for="question">Pregunta: </label>
        <select id="question" v-model="newVoting.question">
          <option v-for="question in questions" :key="question.id" :value="question">
            {{ question.desc }}
          </option>
        </select>
      </div>
      <div>
        <label for="auths">Auths: </label>
        <select id="auths" v-model="newVoting.auths" multiple>
          <option v-for="auth in auths" :key="auth.id" :value="auth">
            {{ auth.name }}
          </option>
        </select>
      </div>
      <div>
        <button class="little-button" @click="changeEditing(false)">Cancelar</button>
        <button class="little-button" @click="guardarVotacion(newVoting)">Guardar</button>
      </div>  
    </div>
  </div>
</template>

<style scoped>

.bold{
  font-weight: bold;
  color: #ffffff;
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
</style>