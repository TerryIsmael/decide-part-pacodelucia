<script>
import { ref, onMounted } from "vue";
import {Question,Option} from "../../models/Question.js";

export default {
  setup() {
    const questions = ref({});
    const selectedQuestion = ref(null);
    const New = ref("New");
    const editing = ref(false);
    const newQuestion = ref(new Question("", []));
    const newOption = ref(new Option());

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

    const saveQuestion = (question) => {
      editing.value = false;
      //TODO: Añadir post y volver a llamar al fetch
      newQuestion.value = new Question("", []);
    };

    const changeSelected = (id) => {
        selectedQuestion.value =
        selectedQuestion.value === id ? null : id;
    };

    const changeEditing = (newValue) => {
      editing.value = newValue;
    };

    const addOption = (question) => {
      question.options.push(newOption.value);
      newOption.value = new Option();
    };

    const removeOption = (question, option) => {
        const index = question.options.indexOf(option);
        if (index !== -1) {
            question.options.splice(index, 1);
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
      newQuestion,
      removeOption,
    };
  },
};
</script>

<template>
  <div>
    <h2>Listado de preguntas</h2>
    <ul>
      <li>
        <button class="little-button" @click="changeSelected(New);changeEditing(true)">
          Nueva pregunta
        </button>
        <div v-if="selectedQuestion == New && editing == true">
        <div>
            <label class="questionDescLabel" for="desc">Descripción:</label>
            <textarea id="desc" rows="10" columns="90" v-model="newQuestion.desc"></textarea>
            
            <form @submit.prevent="saveQuestion(newQuestion)">
                <div v-for="option in newQuestion.options">
                    <label for="optionNumber">Id: </label>
                    <input type="number" id="optionNumber" min="1" v-model="option.number" required/>
                    <label for="option">Opción: </label>
                    <input type="text" id="option" v-model="option.option" required/>
                    <button class="button-inline  little-button" @onclick="removeOption(option)">Eliminar</button>
                </div>
                <p>Nueva opción</p>
                <form @submit.prevent="addOption(newQuestion)">
                        <label for="optionNumber">Id: </label>
                        <input type="number" id="optionNumber" min="1" v-model="newOption.number" required/>
                        <label for="option">Opción: </label>
                        <input type="text" id="option" v-model="newOption.option" required/>
                    <button type="submit" class="little-button button-inline">
                      Añadir
                    </button>
                </form>
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
          <button @click="changeSelected(question.id);changeEditing(false);"> {{ question.desc }} </button>
        </h3>
        <div v-if="selectedQuestion === question.id">
          <div v-if="!editing">
            <p><span class="bold">Descripción:</span> {{ question.desc }}</p>

            <table>
              <tr>
                <th>Número opción</th>
                <th>Opción</th>
              </tr>

              <tr v-for="option in question.options">
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
                <label class = "questionDescLabel" for="desc">Descripción: </label>
                <textarea id="desc" rows="10" columns="90" v-model="question.desc"></textarea>  
                <div v-for="option in question.options">
                    <label for="optionNumber">Id: </label>
                    <input type="number" id="optionNumber" v-model="option.number" required/>
                    <label for="option">Opción: </label>
                    <input type="text" id="option" v-model="option.option" required/>
                    <button class="button-inline  little-button" @onclick="removeOption(option)">Eliminar</button>
                </div>
                <p>Nueva opción</p>
                <form @submit.prevent="addOption(question)">
                        <label for="optionNumber">Id: </label>
                        <input type="number" id="optionNumber" min="1" v-model="newOption.number" required/>
                        <label for="option">Opción: </label>
                        <input type="text" id="option" v-model="newOption.option" required/>
                    <button type="submit" class="little-button button-inline">
                        Añadir
                    </button>
                </form>
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

</style>
