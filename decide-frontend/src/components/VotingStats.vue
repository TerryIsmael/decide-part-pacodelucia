<script>
import { ref, onMounted, computed } from 'vue';
import Voting from '../../models/Voting.js';

//TODO: Cambiar estado de votacion, cambiar preguntas y auths (redireccionar) y conseguir el post

export default {

  setup() {
    const votaciones = ref([]);
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

    const votacionesConFechaInicio = computed(() => {
      return votaciones.value.filter(votacion => votacion.start_date !== null);
    });

    const votacionesConFechaFin = computed(() => {
      return votaciones.value.filter(votacion => votacion.end_date !== null);
    });




 

    onMounted(fetchVotaciones);
    
    return {
      votaciones,
      votacionSeleccionada,
      New,
      editing,
      questions,
      auths,
      newVoting,
      votacionesConFechaInicio,
      votacionesConFechaFin,
    };
  },
};
</script>

<template>
  <div>
    <h2>Datos de Votaciones</h2>
    <table>
      <thead>
        <tr>
          <th>Descripción</th>
          <th>Cantidad</th>
          <th>Ejemplos</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Total de votaciones:</td>
          <td>{{ votaciones.length }}</td>
          <td>
            <ul>
              <template v-for="(votacion, index) in votaciones">
                <li v-if="index < 3" :key="votacion.id">
                  {{ votacion.name }}
                  <template v-if="index < votaciones.length - 1 && index < 2">,</template>
                  <template v-if="index === 2 && votaciones.length > 3"> y más...</template>
                  <template v-if="index === votaciones.length - 1 && votaciones.length <= 3"></template>
                </li>
              </template>
            </ul>
          </td>
        </tr>
        <tr>
          <td>Votaciones con fecha de inicio:</td>
          <td>{{ votacionesConFechaInicio.length }}</td>
          <td>
            <ul>
              <template v-for="(votacion, index) in votacionesConFechaInicio">
                <li v-if="index < 3" :key="votacion.id">
                {{ votacion.name }}
                  <template v-if="index < votacionesConFechaInicio.length - 1 && index < 2">,</template>
                  <template v-if="index === 2 && votacionesConFechaInicio.length > 3"> y más...</template>
                  <template v-if="index === votacionesConFechaInicio.length - 1 && votacionesConFechaInicio.length <= 3"></template>
                </li>
              </template>
            </ul>
          </td>
        </tr>
        <tr>
          <td>Votaciones con fecha de fin:</td>
          <td>{{ votacionesConFechaFin.length }}</td>
          <td>
            <ul>
              <template v-for="(votacion, index) in votacionesConFechaFin">
                <li v-if="index < 3" :key="votacion.id">
                {{ votacion.name }}
                  <template v-if="index < votacionesConFechaFin.length - 1 && index < 2 ">,</template>
                  <template v-if="index === 2 && votacionesConFechaFin.length > 3"> y más...</template>
                  <template v-if="index === votacionesConFechaFin.length - 1 && votacionesConFechaFin.length <= 3"></template>
                </li>
              </template>
            </ul>
          </td>
        </tr>
      </tbody>
    </table>
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