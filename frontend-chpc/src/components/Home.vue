<template>
  <div>
    <!-- Header con logo, barra de búsqueda y enlaces de sesión -->
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

    <!-- Carrusel de Banners -->
    <div v-if="banners.length > 0" class="carousel">
      <div
        v-for="(banner, index) in banners"
        :key="banner.id"
        :class="['carousel-item', { active: index === activeBanner }]"
      >
        <!-- Ajustar la URL para incluir el dominio y puerto del backend -->
        <img :src="getFullImageUrl(banner.imagen_url)" :alt="banner.titulo" class="banner-image" />
        
      </div>
      <button class="prev" @click="cambiarBanner(-1)">❮</button>
      <button class="next" @click="cambiarBanner(1)">❯</button>
    </div>

    <!-- Contenido principal -->
    <div class="home-container">
      <h1>Bienvenidos a Nuestra Tienda</h1>
      <p>Explora nuestros productos y encuentra lo que necesitas.</p>
      <div class="product-grid">
        <div
          v-for="producto in productos"
          :key="producto.id"
          class="product-card"
        >
          <img :src="producto.imagen_url || 'ruta-imagen-default.png'" alt="Imagen del Producto" />
          <h3>{{ producto.nombre_producto }}</h3>
          <p>{{ producto.descripcion }}</p>
          <p v-if="isAuthenticated"><strong>Precio:</strong> ${{ producto.precio }}</p>
          <button v-if="isAuthenticated" @click="verDetalle(producto.id)">Ver Detalles</button>
          <button v-else @click="redirigirLogin">Inicia Sesión para Ver Precios</button>
        </div>
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
      banners: [], // Lista de banners obtenidos del backend
      activeBanner: 0, // Índice del banner actualmente visible
      productos: [], // Lista de productos obtenidos del backend
      searchQuery: '', // Término de búsqueda
      isAuthenticated: false, // Estado de autenticación
    };
  },
  async created() {
    // Comprobación de autenticación
    this.isAuthenticated = !!localStorage.getItem('access_token');

    // Cargar banners desde la API
    try {
      const bannersResponse = await axios.get('http://localhost:5000/tienda/banners');
      this.banners = bannersResponse.data.data;
    } catch (error) {
      console.error('Error al cargar los banners:', error);
    }

    // Cargar productos desde la API
    try {
      const productosResponse = await axios.get('http://localhost:5000/tienda/productos');
      this.productos = productosResponse.data;
    } catch (error) {
      console.error('Error al cargar los productos:', error);
      alert('Hubo un problema al cargar los productos. Intenta de nuevo más tarde.');
    }
  },
  methods: {
    // Construir la URL completa para las imágenes
    getFullImageUrl(relativeUrl) {
      return `http://localhost:5000${relativeUrl}`;
    },
    cambiarBanner(direccion) {  
      this.activeBanner = (this.activeBanner + direccion + this.banners.length) % this.banners.length;
    },
    verDetalle(id) {
      if (id) {
        this.$router.push({ name: 'ProductoDetalle', params: { id } });
      } else {
        console.error('El ID del producto es indefinido.');
      }
    },
    buscarProductos() {
      if (this.isAuthenticated && this.searchQuery.trim() !== '') {
        this.productos = this.productos.filter(producto =>
          producto.nombre_producto.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
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

.user-actions a,
.user-actions button {
  margin-left: 15px;
  color: #ff9900;
  text-decoration: none;
  background: none;
  border: none;
  cursor: pointer;
}

.user-actions a:hover,
.user-actions button:hover {
  text-decoration: underline;
}

/* Estilos del carrusel */
.carousel {
  position: relative;
  width: 100%;
  max-width: 1200px;
  margin: 20px auto;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  height: 400px; /* Ajusta según el tamaño del banner */
}

.carousel-item {
  display: none;
  position: absolute;
  width: 100%;
  height: 100%;
  transition: opacity 0.5s ease-in-out;
}

.carousel-item.active {
  display: block;
  opacity: 1;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ajusta la imagen al contenedor */
}

.carousel-caption {
  position: absolute;
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  color: white;
  background-color: rgba(0, 0, 0, 0.7);
  padding: 15px 20px;
  border-radius: 8px;
  font-size: 1.5rem;
  text-align: center;
}

.carousel .prev,
.carousel .next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 30px;
  color: white;
  background-color: rgba(0, 0, 0, 0.6);
  border: none;
  padding: 10px;
  cursor: pointer;
  border-radius: 50%;
}

.carousel .prev:hover,
.carousel .next:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.carousel .prev {
  left: 10px;
}

.carousel .next {
  right: 10px;
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
