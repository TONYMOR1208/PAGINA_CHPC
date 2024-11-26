<template>
  <!-- Header con diseño original -->
  <header class="header">
    <div class="logo">
      <img src="ruta-del-logo.png" alt="Logo de la Tienda" />
    </div>

    <div class="search-bar">
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Buscar productos..."
        :disabled="!isAuthenticated"
      />
      <button @click="buscarProductos" :disabled="!isAuthenticated">Buscar</button>
    </div>

    <div class="user-actions">
      <template v-if="!isAuthenticated">
        <router-link to="/login">Iniciar Sesión</router-link>
        <router-link to="/registro">Registrarse</router-link>
      </template>
      <template v-else>
        <button @click="cerrarSesion">Cerrar Sesión</button>
      </template>
    </div>
  </header>

  <!-- Contenido principal de la página -->
  <div class="home-container">
    <!-- Nueva sección de banners corredizos -->
    <div class="banner-slider">
      <div v-for="(banner, index) in banners" :key="index" class="banner-slide">
        <img :src="banner.imagen_url" alt="Banner" />
      </div>
    </div>

    <h1>Bienvenidos a Nuestra Tienda</h1>
    <p>Explora nuestros productos y encuentra lo que necesitas.</p>

    <div class="product-grid">
      <div
        v-for="producto in productos"
        :key="producto.id"
        class="product-card"
      >
        <img :src="producto.imagen_url" alt="Imagen del Producto" />
        <h3>{{ producto.nombre }}</h3>
        <p>{{ producto.descripcion }}</p>
        <!-- Muestra el precio solo si el usuario está autenticado -->
        <p v-if="isAuthenticated"><strong>Precio:</strong> ${{ producto.precio }}</p>
        <!-- Muestra el botón de detalles si el usuario está autenticado -->
        <button v-if="isAuthenticated" @click="verDetalle(producto.id)">Ver Detalles</button>
        <!-- Muestra un botón para iniciar sesión si el usuario no está autenticado -->
        <button v-else @click="redirigirLogin">Inicia Sesión para Ver Precios</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      productos: [],
      banners: [], // Nueva propiedad para los banners
      searchQuery: '',
      isAuthenticated: false,
    };
  },
  async created() {
    // Comprobación de autenticación
    this.isAuthenticated = !!localStorage.getItem('access_token');

    // Cargar productos desde la API
    try {
      const response = await axios.get('http://localhost:5000/tienda/productos');
      this.productos = response.data.data;
    } catch (error) {
      console.error("Error al cargar los productos:", error);
    }

    // Cargar banners desde la API
    try {
      const bannerResponse = await axios.get('http://localhost:5000/tienda/banners');
      this.banners = bannerResponse.data.data; // Ajusta según el formato de los datos devueltos
    } catch (error) {
      console.error("Error al cargar los banners:", error);
    }
  },
  methods: {
    verDetalle(id) {
      if (id) {
        this.$router.push({ name: 'ProductoDetalle', params: { id } });
      } else {
        console.error("El ID del producto es indefinido.");
      }
    },
    buscarProductos() {
      if (this.isAuthenticated) {
        console.log("Buscando productos con:", this.searchQuery);
        // Agrega aquí la lógica de búsqueda
      }
    },
    cerrarSesion() {
      localStorage.removeItem('access_token');
      this.isAuthenticated = false;
      this.$router.replace('/login');
    },
    redirigirLogin() {
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
/* Estilos del header original */
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

.search-bar {
  display: flex;
  align-items: center;
}

.search-bar input {
  padding: 8px;
  border: none;
  border-radius: 5px 0 0 5px;
}

.search-bar button {
  padding: 8px 12px;
  border: none;
  background-color: #ff9900;
  color: white;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
}

.search-bar button:hover:enabled {
  background-color: #ff8c00;
}

.user-actions a, .user-actions button {
  margin-left: 15px;
  color: #ff9900;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
}

.user-actions a:hover, .user-actions button:hover {
  text-decoration: underline;
}

/* Estilos del slider de banners */
.banner-slider {
  display: flex;
  overflow-x: scroll;
  gap: 20px;
  margin-bottom: 20px;
}

.banner-slide {
  min-width: 300px;
  max-width: 100%;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.banner-slide img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

/* Estilos del contenido principal */
.home-container {
  text-align: center;
  margin: 30px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.product-card img {
  max-width: 100%;
  border-radius: 8px;
}

.product-card h3 {
  font-size: 18px;
  margin: 10px 0;
}

.product-card p {
  font-size: 14px;
  color: #333;
}

.product-card button {
  padding: 10px 20px;
  background-color: #ff9900;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.product-card button:hover {
  background-color: #ff8c00;
}
</style>
