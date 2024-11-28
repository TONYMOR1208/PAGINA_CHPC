<template>

    <header class="header">
        <div class="logo">
          <img src="ruta-del-logo.png" alt="Logo de la Tienda" />
        </div>
        <div class="navigation">
          <!-- Botón para ir a la página principal con restricciones -->
          <router-link to="/">Ir a la página principal</router-link>
        </div>
      </header>
  
    <div class="register-container">
      <h2>Crear Una Cuenta</h2>
      <p><router-link to="/">Inicio</router-link> / Registro</p>
  
      <form @submit.prevent="register">
        <div class="input-group">
          <label for="nombre_usuario">Nombre de usuario *</label>
          <input
            v-model="nombre_usuario"
            id="nombre_usuario"
            type="text"
            placeholder="Nombre de usuario"
            required
            @input="clearError('nombre_usuario')"
          />
          <p v-if="errors.nombre_usuario" class="error">{{ errors.nombre_usuario }}</p>
        </div>
  
        <div class="input-group">
          <label for="email">Dirección de correo electrónico *</label>
          <input
            v-model="email"
            id="email"
            type="email"
            placeholder="Correo electrónico"
            required
            @input="clearError('email')"
          />
          <p v-if="errors.email" class="error">{{ errors.email }}</p>
        </div>
  
        <div class="input-group">
          <label for="telefono">Teléfono</label>
          <input
            v-model="telefono"
            id="telefono"
            type="text"
            placeholder="Número de teléfono"
            @input="clearError('telefono')"
          />
          <p v-if="errors.telefono" class="error">{{ errors.telefono }}</p>
        </div>
  
        <div class="input-group">
          <label for="direccion">Dirección</label>
          <input
            v-model="direccion"
            id="direccion"
            type="text"
            placeholder="Dirección"
            @input="clearError('direccion')"
          />
          <p v-if="errors.direccion" class="error">{{ errors.direccion }}</p>
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
              @input="clearError('contraseña')"
            />
            <span class="toggle-password" @click="togglePasswordVisibility">
              {{ passwordVisible ? '👁️' : '🙈' }}
            </span>
          </div>
          <p v-if="errors.contraseña" class="error">{{ errors.contraseña }}</p>
        </div>
  
        <button type="submit" class="register-button">Registrarse</button>
  
        <p>¿YA TIENE UNA CUENTA? <router-link to="/login">INICIE SESIÓN AQUÍ</router-link></p>
      </form>
  
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="success" class="success">{{ success }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        nombre_usuario: '',
        email: '',
        telefono: '',
        direccion: '',
        contraseña: '',
        errors: {},
        error: '',
        success: '',
        passwordVisible: false,
      };
    },
    methods: {
      async register() {
        this.validateFields();
        if (Object.keys(this.errors).length > 0) {
          return;
        }
        try {
          const response = await axios.post('http://localhost:5000/tienda/auth/registro', {
            nombre_usuario: this.nombre_usuario,
            email: this.email,
            telefono: this.telefono,
            direccion: this.direccion,
            contraseña: this.contraseña,
          });
          this.success = response.data.mensaje;
          this.clearForm();
        } catch (err) {
          this.error = err.response?.data?.mensaje || 'Error en el registro. Intenta de nuevo.';
        }
      },
      validateFields() {
        this.errors = {};
        if (this.nombre_usuario.length < 3 || this.nombre_usuario.length > 80) {
          this.errors.nombre_usuario = 'El nombre de usuario debe tener entre 3 y 80 caracteres.';
        }
        if (!this.email.includes('@')) {
          this.errors.email = 'El correo electrónico debe tener un formato válido.';
        }
        if (this.telefono && this.telefono.length > 20) {
          this.errors.telefono = 'El teléfono debe tener como máximo 20 caracteres.';
        }
        if (this.direccion && this.direccion.length > 255) {
          this.errors.direccion = 'La dirección debe tener como máximo 255 caracteres.';
        }
        if (!this.contraseña.match(/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/)) {
          this.errors.contraseña = 'La contraseña debe tener al menos 6 caracteres, incluir una letra, un número y un carácter especial.';
        }
      },
      clearError(field) {
        delete this.errors[field];
      },
      togglePasswordVisibility() {
        this.passwordVisible = !this.passwordVisible;
      },
      clearForm() {
        this.nombre_usuario = '';
        this.email = '';
        this.telefono = '';
        this.direccion = '';
        this.contraseña = '';
        this.errors = {};
      },
    },
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
  /* Los estilos permanecen iguales */
  .register-container {
    max-width: 500px;
    margin: 50px auto;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    font-family: 'Amazon Ember', sans-serif;
  }
  
  .register-container h2 {
    text-align: center;
    color: #131921;
    font-size: 22px;
  }
  
  .register-container p {
    text-align: center;
    font-size: 14px;
    color: #666;
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
  
  .register-button {
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
  
  .register-button:hover {
    background-color: #ff8c00;
  }
  
  .error {
    color: #ff0000;
    text-align: center;
    font-weight: bold;
  }
  
  .success {
    color: #28a745;
    text-align: center;
    font-weight: bold;
  }
  
  .register-container a {
    color: #ff9900;
    text-decoration: none;
  }
  
  .register-container a:hover {
    text-decoration: underline;
  }
  </style>
  