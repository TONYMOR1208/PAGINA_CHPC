<template>
    <div>
      <!-- Header con opción para ir a la página principal -->
      <header class="header">
        <div class="logo">
          <img src="ruta-del-logo.png" alt="Logo de la Tienda" />
        </div>
        <div class="navigation">
          <!-- Botón para ir a la página principal con restricciones -->
          <router-link to="/">Ir a la página principal</router-link>
        </div>
      </header>
  
      <!-- Contenedor de inicio de sesión -->
      <div class="login-container">
        <h2>Iniciar Sesión</h2>
        <form @submit.prevent="login">
          <div class="input-group">
            <label for="nombre_usuario">Escriba su nombre de usuario</label>
            <input
              v-model="nombre_usuario"
              id="nombre_usuario"
              type="text"
              placeholder="Nombre de usuario"
              required
              @input="clearError"
            />
          </div>
  
          <div class="input-group">
            <label for="contraseña">Contraseña *</label>
            <div class="password-container">
              <input
                v-model="contraseña"
                id="contraseña"
                :type="passwordVisible ? 'text' : 'password'"
                placeholder="Contraseña"
                required
                @input="clearError"
              />
              <span class="toggle-password" @click="togglePasswordVisibility">
                {{ passwordVisible ? '👁️' : '🙈' }}
              </span>
            </div>
          </div>
  
          <button type="submit" class="login-button">Iniciar sesión</button>
          <button class="create-account-button" @click="goToRegister">Crear cuenta</button>
        </form>
  
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        nombre_usuario: '',
        contraseña: '',
        error: '',
        passwordVisible: false
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://localhost:5000/tienda/auth/login', {
            nombre_usuario: this.nombre_usuario,
            contraseña: this.contraseña
          });
          localStorage.setItem('access_token', response.data.access_token); // Guarda el token en localStorage
          this.$router.replace('/home'); // Usa replace en lugar de push
        } catch (err) {
          this.error = "Credenciales inválidas. Intenta de nuevo.";
        }
      },
      clearError() {
        this.error = '';
      },
      togglePasswordVisibility() {
        this.passwordVisible = !this.passwordVisible;
      },
      goToRegister() {
        this.$router.push('/registro');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Estilos del header */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    background-color: #232f3e;
    color: white;
  }
  
  .logo img {
    width: 100px;
  }
  
  .navigation a {
    color: #ff9900;
    text-decoration: none;
    font-size: 16px;
  }
  
  .navigation a:hover {
    text-decoration: underline;
  }
  
  /* Estilos del contenedor de inicio de sesión */
  .login-container {
    max-width: 360px;
    margin: 50px auto;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    font-family: 'Amazon Ember', sans-serif;
  }
  
  .login-container h2 {
    text-align: center;
    font-size: 22px;
    color: #131921;
    margin-bottom: 20px;
  }
  
  .input-group {
    margin-bottom: 15px;
  }
  
  .input-group label {
    font-size: 14px;
    color: #333;
    margin-bottom: 5px;
    display: block;
  }
  
  .input-group input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
    background-color: #fff;
  }
  
  .input-group input:focus {
    border-color: #ff9900;
    outline: none;
  }
  
  .password-container {
    position: relative;
  }
  
  .toggle-password {
    position: absolute;
    top: 50%;
    right: 10px;
    transform: translateY(-50%);
    font-size: 20px;
    cursor: pointer;
  }
  
  .login-button {
    width: 100%;
    padding: 12px;
    background-color: #ff9900;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    margin-top: 15px;
  }
  
  .login-button:hover {
    background-color: #ff8c00;
  }
  
  .create-account-button {
    width: 100%;
    padding: 12px;
    background-color: #232f3e;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 10px;
  }
  
  .create-account-button:hover {
    background-color: #1d2631;
  }
  
  .error {
    color: #ff0000;
    text-align: center;
    font-weight: bold;
    margin-top: 10px;
  }
  </style>