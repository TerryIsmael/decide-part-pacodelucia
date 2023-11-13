<script>
import { ref, onMounted } from 'vue';
import CreateOrEditVoting from './CreateOrEditVoting.vue';

export default {

  setup() {
    const votaciones = ref({});
    const votacionSeleccionada = ref(null);
    const New = ref("New");

    const fetchVotaciones = async () => {
      try {
        const response = await fetch('http://localhost:8000/voting/');
        const data = await response.json();
        votaciones.value = data;
      } catch (error) {
        console.error('Error:', error);
      }
    };

    onMounted(fetchVotaciones);

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
    }

    return {
      votaciones,
      votacionSeleccionada,
      mostrarFormulario,
      agregarVotacion,
      cambiarSeleccionada,
      formatearFecha,
      isNumberInTally,
      New,
    };
  },
  components: {
    CreateOrEditVoting,
  },
};
</script>

<template>
  <div>
    <h2>Listado de Votaciones</h2>
    <ul>
      <li v-for="votacion in votaciones" :key="votacion.id">

        <h3>
          <button @click="cambiarSeleccionada(votacion.id)">{{ votacion.name }} - {{ formatearFecha(votacion.start_date)
          }} {{ formatearFecha(votacion.end_date) }}</button>
        </h3>

        <div v-if="votacionSeleccionada === votacion.id">
          <p> Id: {{ votacion.id }} </p>
            <p> Descripción: {{ votacion.desc }} </p>
            <p> Pregunta: {{ votacion.question.desc }} </p>

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

            <h4>- AUTHS -</h4>
            <table>
              <tr>
                <th> Nombre </th>
                <th> URL </th>
                <th> Yo </th>
              </tr>
              <tr v-for="auth in votacion.auths">
                <td> {{ auth.name }} </td>
                <td> {{ auth.url }} </td>
                <td> {{ auth.me }} </td>
              </tr>
            </table>

          <p> Fecha inicio: {{ formatearFecha(votacion.start_date) }} </p>
          <p v-if="votacion.end_date != null"> Fecha fin: {{ formatearFecha(votacion.end_date) }} </p>
          <h4 v-if="votacion.postproc == null">No finalizada - no hay postprocesado</h4>

          <h4>- PUB_KEY -</h4>
          <p> P: {{ BigInt(votacion.pub_key.p) }} </p>
          <p> G: {{ BigInt(votacion.pub_key.g) }} </p>
          <p> Y: {{ BigInt(votacion.pub_key.y) }} </p>

          <p>Opción ganadora: {{ votacion.tally ? votacion.tally.toString() : 'No hay recuento' }}</p>
        </div>
      </li>
    </ul>

    <button class="little-button" @click="mostrarFormulario(New)">Crear Nueva Votación</button>
  </div>
</template>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

table {
  width: 60%;
  border-collapse: collapse;
  margin: auto;
  margin-bottom: 20px;
}

th,td,tr {
  border: 1px solid black;
  background-color: #008b8b;
  color: rgb(255, 255, 255);
  padding: 8px;
  width: 33%;
  text-align: center;
}

th {
  background-color: #024a4a;
}

.remarkable td {
  background-color: rgba(178, 117, 87, 0.868);
}

label {
  display: block;
  margin-bottom: 5px;
  text-align: center;
  color: white; 
}

#auths, input, textarea, select  {
  background-color: #3b3b3b;
  height: 30px;
  margin-bottom: 20px;
  padding: 5px;
  border-radius: 5px;
  border: 2px solid grey;
  width: 67%;
}

input {
  height: 25px;
  width: 65%;
}

textarea {
  height: 60px;
  width: 65%;
}

select option:checked{
  background-color: #027d7d;
}

#auths {
  height: 60px;
  width: 67%;
}
.form-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  overflow: hidden;
}
.form-div > form {
  width: 400px;
  padding: 40px;
  border-radius: 5px;
  background-color: rgb(255, 255, 255);
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.little-button {
  background-color: rgb(0, 139, 86);
  color: rgb(255, 255, 255);
  padding: 8px;
  text-align: center;
  border: none;
  cursor: pointer;
  width: 30%;
  margin-bottom: 10px;
}

button {
  background-color: rgb(0, 139, 139);
  color: rgb(255, 255, 255);
  padding: 8px;
  text-align: center;
  border: none;
  cursor: pointer;
  width: 100%;
  margin-bottom: 10px;
}  

</style>