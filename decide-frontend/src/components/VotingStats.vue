<script>
import { ref, onMounted, computed, watchEffect, watch } from 'vue';
import Voting from '../../models/Voting.js';



export default {

  setup() {
    const votaciones = ref([]);
    const votacionSeleccionada = ref(null);
    const New = ref("New");
    const editing = ref(false);
    const questions = ref([]);
    const auths = ref([]);
    const newVoting = ref(new Voting());
    const totalDistinctQuestions = ref(0);
  

    const fetchVotaciones = async () => {
      try {
        const response = await fetch('http://localhost:8000/voting/');
        const data = await response.json();
        votaciones.value = data;
        // Aquí se realiza la obtención de all-auths y all-questions
        const questionResponse = await fetch('http://localhost:8000/voting/all-questions/', {
          method: 'GET',
          credentials: 'include'
        });
        const questionData = await questionResponse.json();
        console.log('Fetched questions:', questionData);
        questions.value = questionData;
        totalDistinctQuestions.value = countDistinctQuestions(questionData);
        

        const authResponse = await fetch('http://localhost:8000/voting/all-auths/', {
          method: 'GET',
          credentials: 'include'
        });
        const authData = await authResponse.json();
        auths.value = authData;
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

    const totalDistinctAuths = computed(() => {
      const distinctAuths = new Set();
      votaciones.value.forEach((votacion) => {
        votacion.auths.forEach((auth) => {
          distinctAuths.add(auth.name);
        });
      });
      return distinctAuths.size;
    });

    const countDistinctQuestions = (data) => {
      if (data.length === 0) {
        return 0;
      }
  
      const distinctQuestions = new Set();
      data.forEach((question) => {
        distinctQuestions.add(question.desc);
      });
      return distinctQuestions.size;
    };


    


  



 

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
      totalDistinctAuths,
      totalDistinctQuestions,
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
        <tr>
          <td>Total de auths distintos:</td>
          <td>{{ totalDistinctAuths }}</td>
          <td>
            <ul>
              <template v-for="(auth, index) in auths" :key="index">
                <li v-if="index < 3">
                  {{ auth.name }}
                  <template v-if="index < auths.length - 1 && index < 2">,</template>
                  <template v-if="index === 2 && auths.length > 3"> y más...</template>
                  <template v-if="index === auths.length - 1 && auths.length <= 3"></template>
                </li>
              </template>
            </ul>
          </td>
        </tr>
        <tr>
          <td>Total de preguntas distintas:</td>
          <td>{{ totalDistinctQuestions }}</td>
          <td>
            <ul>
              <template v-for="(question, index) in questions" :key="index">
                <li v-if="index < 3">
                  {{ question.desc }}
                  <template v-if="index < questions.length - 1 && index < 2">,</template>
                  <template v-if="index === 2 && questions.length > 3"> y más...</template>
                  <template v-if="index === questions.length - 1 && questions.length <= 3"></template>
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