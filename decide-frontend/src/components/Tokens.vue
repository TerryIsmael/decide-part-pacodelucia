<template>
    <div>
        <h1 id="title">Tokens</h1>
        <table>
            <thead>
                <tr>
                <th>Token</th>
                <th>Usuario</th>
                <th>Fecha</th>
                <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="token in tokens" :key="token.id">
                    <td>{{ token.token }}</td>
                    <td>{{ token.user }}</td>
                    <td>{{ token.date }}</td>
                    <td v-if="token.token != ''">
                        <button class="button-delete" @click="deleteToken(token.id)">Eliminar</button>
                    </td>
                    <td v-else>
                        <button class="button-add" @click="addToken(token.id)">Añadir</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p> {{ tokens.length }} tokens</p>
    </div>
</template>

<script>
export default {
    name: 'Tokens',
    data() {
        return {
            token: '',
            tokens: []
        };
    },
    mounted() {
        this.getTokens();
    },
    methods: {
        init() {
            var cookies = document.cookie.split(';');
            cookies.forEach(cookie => {
                var cookiePair = cookie.split('=');
                if (cookiePair[0].trim() === 'sessionid' && cookiePair[1]) {
                    this.token = pair[1];
                    this.getTokens();
                }
            });

        },
        async getTokens() {
            try {
                const response = await fetch('http://localhost:8000/authentication/get-auth/', {
                    credentials: 'include',
                });
                if (response.ok) {
                    const data = await response.json();
                    this.tokens = data.tokens;
                } else {
                    throw new Error('Usuario o contraseña incorrectos');
                }
            } catch (error) {
                console.log(error);
            }  
        },
        async deleteToken(userId) {
            try {
                const response = await fetch(`http://localhost:8000/authentication/del-auth/${userId}`, {
                    credentials: 'include',
                });
                if (response.ok) {
                    await this.getTokens();
                } else {
                    throw new Error('No se pudo eliminar el token');
                }
            } catch (error) {
                console.log(error);
                alert('No se pudo eliminar el token');
            }
        },
        async addToken(userId) {
            try {
                const response = await fetch(`http://localhost:8000/authentication/add-auth/${userId}`, {
                    credentials: 'include',
                });
                if (response.ok) {
                    await this.getTokens();
                } else {
                    throw new Error('No se pudo eliminar el token');
                }
            } catch (error) {
                console.log(error);
                alert('No se pudo eliminar el token');
            }
        }
    }
};
</script>

<style scoped>
#title {
    font-family: 'Roboto', sans-serif;
    font-size: 40px;
    font-weight: 700;
    text-align: left;
}

thead {
    background-color: #f2f2f24d;

}

table, th, td {
  border: none;
}

table {
    width: 100%;
}

th, td {
  text-align: left;
  padding: 8px;
}

p {
    text-align: left;
    color: rgb(196, 195, 195);
}

.button-delete {
    background-color: rgb(211, 91, 91);
    
    width: 100%;
}

.button-add {
    background-color: rgb(91, 211, 91);
    width: 100%;
}

</style>