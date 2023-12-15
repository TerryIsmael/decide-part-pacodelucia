<script>
import { ref, onMounted, inject } from "vue";
import { Option } from "../../models/Question.js";


export default {
  setup() {
    const questions = ref({});
    const selectedQuestion = ref(null);
    const New = ref("New");
    const editing = ref(false);
    const newOption = ref(new Option());
    const newOptions = ref([]);
    const newOptionError = ref(null);
    const optionError = ref(null);
    const newDesc = ref("");
    const logged = inject("logged");
    const navBarLoaded = inject('navBarLoaded')
    
    const init = async () => {
      while (!navBarLoaded.value) {
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      navBarLoaded.value = false; 
      if (logged.value) {
        //Init functions
        fetchQuestions();
      }
    }
    
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

    const saveQuestion = async () => {

      if (newDesc.value === undefined || newDesc.value.trim() === "" || newOptions.value.length === 0) {
        optionError.value = ("No se puede guardar una pregunta vacía o sin opciones");
        return;
      }
      else
        optionError.value = null;

      newOptionError.value = null;
      newOptions.value.forEach((option) => {
        if (option.number <= 0)
          optionError.value = ("No se puede añadir una opción con id menor que 1");
      });

      if (optionError.value != null || newOptionError.value != null)
        return;
      editing.value = false;

      const newQuestion = {
        id: selectedQuestion.value == "New" ? null : selectedQuestion.value,
        desc: newDesc.value,
        options: newOptions.value,
      };

      try {
        await fetch(import.meta.env.VITE_API_URL + "/voting/all-questions/", {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newQuestion),
        });
      } catch (error) {
        console.error("Error:", error);
      }
      newDesc.value = "";
      newOptions.value = new Option();
      await fetchQuestions();
    };

    const changeSelected = (questionId) => {
      selectedQuestion.value = selectedQuestion.value === questionId ? null : questionId;
    };

    const changeEditing = (newValue) => {
      if (newValue === false || selectedQuestion.value === "New" || selectedQuestion.value === null) {
        newDesc.value = "";
        newOptions.value = [];
      }
      else {
        newDesc.value = questions.value.find(x => x.id == selectedQuestion.value).desc;
        newOptions.value = [].concat(questions.value.find(x => x.id == selectedQuestion.value).options);
      }
      newOptionError.value = null;
      optionError.value = null;
      editing.value = newValue;
    };

    const addOption = () => {
      if (newOption.value.number === undefined || newOption.value.number.toString().trim() === "" || newOption.value.number <= 0 || newOption.value.option === undefined || newOption.value.option.trim() === "")
        newOptionError.value = ("No se puede añadir una opción vacía o con id menor que 1");
      else {
        newOptions.value.push(newOption.value);
        newOption.value = new Option();
        newOptionError.value = null;
      }
    };

    const removeOption = (option) => {
      const index = newOptions.value.indexOf(option);
      if (index !== -1) {
        newOptions.value.splice(index, 1);
      }
    };

    const deleteQuestion = async (id) => {
      const questionDelete = {
        id: id,
      };
      try {
        const response = await fetch(import.meta.env.VITE_API_URL + "/voting/all-questions/",
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify(questionDelete),
          }
        );
      } catch (error) {
        console.error("Error:", response.status, error.json());
      }
      fetchQuestions();
    }

    onMounted(init);

    return {
      questions,
      selectedQuestion,
      New,
      editing,
      newOption,
      newOptions,
      newOptionError,
      optionError,
      newDesc,
      saveQuestion,
      changeSelected,
      changeEditing,
      addOption,
      removeOption,
      deleteQuestion,
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
            <div>
              <p class="bold" style="color:rgb(211, 91, 91)">{{optionError}}</p>
            </div>
            <form @submit.prevent="saveQuestion">
              <label class="questionDescLabel" for="desc">Descripción: </label>
              <textarea id="desc" rows="10" columns="90" v-model="newDesc"></textarea>

              <div v-for="option in newOptions">
                <label for="optionNumber">Id: </label>
                <input type="number" id="optionNumber" v-model="option.number" required />
                <label for="option">Opción: </label>
                <input type="text" id="option" v-model="option.option" required />
                <button type="button" class="button-inline little-button delete-button"
                  @click="removeOption(option)">Eliminar</button>
              </div>

              <p>Nueva opción</p>
              <div>
                <p class="bold" style="color:rgb(211, 91, 91)">{{newOptionError}}</p>
              </div>
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
            <button class="little-button delete-button" @click="deleteQuestion(question.id)">
              Eliminar
            </button>
          </div>

          <div v-else>

            <div>
              <p class="bold" style="color:rgb(211, 91, 91)">{{optionError}}</p>
            </div>
            <form @submit.prevent="saveQuestion">
              <label class="questionDescLabel" for="desc">Descripción: </label>
              <textarea id="desc" rows="10" columns="90" v-model="newDesc"></textarea>
              <div v-for="option in newOptions">
                <label for="optionNumber">Id: </label>
                <input type="number" id="optionNumber" v-model="option.number" required />
                <label for="option">Opción: </label>
                <input type="text" id="option" v-model="option.option" required />
                <button type="button" class="button-inline little-button delete-button"
                  @click="removeOption(option)">Eliminar</button>
              </div>

              <p>Nueva opción</p>
              <div>
                <p class="bold" style="color:rgb(211, 91, 91)">{{newOptionError}}</p>
              </div>
              <label for="optionNumber">Id: </label>
              <input type="number" id="optionNumber" min="1" v-model="newOption.number" />
              <label for="newOption">Opción: </label>
              <input type="text" id="newOption" v-model="newOption.option" />
              <button type="button" class="little-button button-inline" @click="addOption">
                Añadir
              </button>

              <button class="little-button" @click="changeEditing(false)">
                Cancelar
              </button>
              <button type="submit" class="little-button">
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

.error {
  background-color: rgb(211, 91, 91);
  color: white;
  display: block;
  border-radius: 8px;
  width: 60%;
  margin-left: auto;
  margin-right: auto;
}
</style>