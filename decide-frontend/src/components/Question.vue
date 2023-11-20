<script>
import { ref, reactive, onMounted } from "vue";
import { Question, Option } from "../../models/Question.js";

export default {
  setup() {
    const questions = ref({});
    const selectedQuestion = ref(null);
    const New = ref("New");
    const editing = ref(false);
    const newQuestion = ref(new Question("", []));
    const newOption = ref(new Option());
    const newOptions = ref([]);
    const dataError = ref(null);

    const fetchquestions = async () => {
      try {
        const response = await fetch("http://localhost:8000/voting/all-questions/", {
          method: "GET",
          credentials: "include",
        });

        const data = await response.json();
        questions.value = data;
      } catch (error) {
        console.error("Error:", error);
      }
    };

    const saveQuestion = async (question) => {
      editing.value = false;
      question.options = [].concat(newOptions.value);
      const questionJson = {
        id: question.id,
        desc: question.desc,
        options: question.options,
      };

      try {
        await fetch("http://localhost:8000/voting/all-questions/", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(question),
        });
      } catch (error) {
        console.error("Error:", error);
      }
      newOptions.value = new Option();
      await fetchquestions();

    };

    const changeSelected = (questionId) => {
      selectedQuestion.value = selectedQuestion.value === questionId ? null : questionId;
    };

    const changeEditing = (newValue) => {
      if (newValue === false || selectedQuestion.value === "New")
        newOptions.value = [];
      else
        newOptions.value = [].concat(questions.value.filter(x => x.id == selectedQuestion.value)[0].options);
      
      dataError.value = null;
      editing.value = newValue;
    };

    const addOption = () => {
      console.log(newOption.value.number);
      if ( newOption.value.number === undefined || newOption.value.option === undefined)
        dataError.value = ("No se puede añadir una opción vacía");
      else{
        newOptions.value.push(newOption.value);
        newOption.value = new Option();
        dataError.value = null;
      }
    };

    const removeOption = (option) => {
      const index = newOptions.value.indexOf(option);
      if (index !== -1) {
        newOptions.value.splice(index, 1);
      }
    };

    onMounted(fetchquestions);

    return {
      questions,
      selectedQuestion,
      New,
      editing,
      saveQuestion,
      changeSelected,
      changeEditing,
      addOption,
      newOption,
      newOptions,
      newQuestion,
      removeOption,
      dataError,
    };
  },
};
</script>

<template>
  <div>
    <h2>Listado de preguntas</h2>
    <ul>
      <li>
        <button class="little-button" @click="changeSelected(New); changeEditing(true)">
          Nueva pregunta
        </button>

        <div v-if="selectedQuestion == New && editing == true">
          <div>
            <form @submit.prevent="saveQuestion(newQuestion)">
              <label class="questionDescLabel" for="desc">Descripción: </label>
              <textarea id="desc" rows="10" columns="90" v-model="newQuestion.desc"></textarea>

              <div v-for="option in newOptions">
                <label for="optionNumber">Id: </label>
                <input type="number" id="optionNumber" v-model="option.number" required />
                <label for="option">Opción: </label>
                <input type="text" id="option" v-model="option.option" required />
                <button type="button" class="button-inline little-button delete-button" @click="removeOption(option)">Eliminar</button>
              </div>
              
              <p>Nueva opción</p>
              <p v-if="dataError != null" class="error">{{ dataError }}</p>
              <label for="newOptionNumber">Id: </label>
              <input type="number" id="newOptionNumber" min="1" v-model="newOption.number" />
              <label for="newOption">Opción: </label>
              <input type="text" id="newOption" v-model="newOption.option" />
              <button type="button" class="little-button button-inline" @click="addOption">
                Añadir
              </button>

              <button class="little-button" @click="changeEditing(false)">
                Cancelar
              </button>
              <button class="little-button" type="submit">
                Guardar
              </button>
            </form>
          </div>
        </div>
      </li>
      <li v-for="question in questions" :key="question.id">
        <h3>
          <button @click="changeSelected(question.id); changeEditing(false);"> {{ question.desc }} </button>
        </h3>
        <div v-if="selectedQuestion === question.id">
          <div v-if="!editing">
            <p><span class="bold">Descripción:</span> {{ question.desc }}</p>
            <table>
              <tr>
                <th>Número opción</th>
                <th>Opción</th>
              </tr>
              <tr v-for="option in question.options" :key="option.number">
                <td>{{ option.number }}</td>
                <td>{{ option.option }}</td>
              </tr>
            </table>

            <button class="little-button" @click="changeEditing(true)">
              Editar
            </button>
          </div>

          <div v-else>
            <form @submit.prevent="saveQuestion(question)">
              <label class="questionDescLabel" for="desc">Descripción: </label>
              <textarea id="desc" rows="10" columns="90" v-model="question.desc"></textarea>
              <div v-for="option in newOptions">
                <label for="optionNumber">Id: </label>
                <input type="number" id="optionNumber" v-model="option.number" required />
                <label for="option">Opción: </label>
                <input type="text" id="option" v-model="option.option" required />
                <button type="button" class="button-inline little-button delete-button" @click="removeOption(option)">Eliminar</button>
              </div>

              <p>Nueva opción</p>
              <p v-if="dataError != null" class="error">{{ dataError }}</p>
                <label for="optionNumber">Id: </label>
                <input type="number" id="optionNumber" min="1" v-model="newOption.number"/>
                <label for="newOption">Opción: </label>
                <input type="text" id="newOption" v-model="newOption.option"/>
                <button type="button" class="little-button button-inline" @click="addOption">
                  Añadir
                </button>

              <button class="little-button" @click="changeEditing(false)">
                Cancelar
              </button>
              <button class="little-button" type="submit">
                Guardar
              </button>
            </form>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
label {
  display: inline-block;
  width: 100px;
  vertical-align: middle;
}

.questionDescLabel {
  display: inline-block;
  margin-bottom: 5px;
  text-align: center;
  color: white;
  vertical-align: top;
}

textarea {
  display: inline-block;
  width: 50%;
  overflow: hidden;
  resize: none;
  vertical-align: top;
}

input {
  display: inline-block;
  width: 200px;
}

.button-inline {
  display: inline-block;
  width: 100px;
  margin: 0 10px;
  vertical-align: top;
}

.delete-button {
  background-color: rgb(211, 91, 91);
}

.error{
  background-color: rgb(211, 91, 91);
  color: white;
  display: block;
  border-radius: 8px;
  width: 60%;
  margin-left: auto;
  margin-right: auto;
}

</style>