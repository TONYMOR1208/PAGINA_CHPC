<template>
  <!-- Header -->
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

  <!-- Contenido principal -->
  <div class="home-container">
    <!-- Banners -->
    <div class="banner-slider">
      <!-- Indicador de carga -->
      <template v-if="loadingBanners">
        <p>Cargando banners...</p>
      </template>
      <!-- Mostrar banners si se cargan correctamente -->
      <template v-else-if="banners.length">
        <div
          v-for="(banner, index) in banners"
          :key="index"
          class="banner-slide"
        >
          <img
            :src="banner.imagen_url"
            :alt="banner.titulo"
            @error="handleImageError($event, banner)"
          />
        </div>
      </template>
      <!-- Mensaje si no hay banners disponibles -->
      <template v-else>
        <p>No hay banners disponibles en este momento.</p>
      </template>
    </div>

    <h1>Bienvenidos a Nuestra Tienda</h1>
    <p>Explora nuestros productos y encuentra lo que necesitas.</p>

    <!-- Productos -->
    <template v-if="loadingProductos">
      <p>Cargando productos...</p>
    </template>
    <template v-else-if="productos.length">
      <div class="product-grid">
        <div
          v-for="producto in productos"
          :key="producto.id"
          class="product-card"
        >
          <img
            :src="producto.imagen_url"
            :alt="producto.nombre"
            @error="handleImageError($event, producto)"
          />
          <h3>{{ producto.nombre }}</h3>
          <p>{{ producto.descripcion }}</p>
          <!-- Mostrar precio solo si está autenticado -->
          <p v-if="isAuthenticated">
            <strong>Precio:</strong> ${{ producto.precio }}
          </p>
          <!-- Botón de acciones según autenticación -->
          <button v-if="isAuthenticated" @click="verDetalle(producto.id)">
            Ver Detalles
          </button>
          <button v-else @click="redirigirLogin">
            Inicia Sesión para Ver Precios
          </button>
        </div>
      </div>
    </template>
    <template v-else>
      <p>No hay productos disponibles en este momento.</p>
    </template>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      productos: [], // Lista de productos
      banners: [], // Lista de banners
      searchQuery: '', // Texto del cuadro de búsqueda
      isAuthenticated: false, // Estado de autenticación
      loadingProductos: false, // Indicador de carga para productos
      loadingBanners: false, // Indicador de carga para banners
      errorProductos: null, // Error al cargar productos
      errorBanners: null, // Error al cargar banners
    };
  },
  async created() {
    // Comprobar si el usuario está autenticado
    this.isAuthenticated = !!localStorage.getItem('access_token');

    // Cargar datos iniciales
    await this.cargarProductos();
    await this.cargarBanners();
  },
  methods: {
    async cargarProductos() {
      this.loadingProductos = true;
      this.errorProductos = null;
      try {
        const response = await axios.get('http://localhost:5000/tienda/productos');
        if (response.data && response.data.data) {
          this.productos = response.data.data;
        } else {
          this.errorProductos = 'Formato inesperado en la respuesta de productos.';
          console.error('Formato inesperado en la respuesta de productos:', response.data);
        }
      } catch (error) {
        this.errorProductos = 'Error al cargar los productos. Inténtalo más tarde.';
        console.error('Error al cargar los productos:', error.message);
      } finally {
        this.loadingProductos = false;
      }
    },
    async cargarBanners() {
      this.loadingBanners = true;
      this.errorBanners = null;
      try {
        const response = await axios.get('http://localhost:5000/tienda/banners');
        if (response.data && response.data.data) {
          this.banners = response.data.data;
        } else {
          this.errorBanners = 'Formato inesperado en la respuesta de banners.';
          console.error('Formato inesperado en la respuesta de banners:', response.data);
        }
      } catch (error) {
        this.errorBanners = 'Error al cargar los banners. Inténtalo más tarde.';
        console.error('Error al cargar los banners:', error.message);
      } finally {
        this.loadingBanners = false;
      }
    },
    handleImageError(event, item) {
      console.error(`Error cargando imagen: ${item.imagen_url}`);
      event.target.src = "/static/default-placeholder.png"; // Imagen predeterminada
    },
    verDetalle(id) {
      if (id) {
        this.$router.push({ name: 'ProductoDetalle', params: { id } });
      } else {
        console.error('El ID del producto es indefinido.');
      }
    },
    buscarProductos() {
      if (this.isAuthenticated && this.searchQuery) {
        console.log('Buscando productos con:', this.searchQuery);
        // Lógica de búsqueda adicional
      } else if (!this.searchQuery) {
        console.warn('Introduce un término de búsqueda.');
      } else {
        console.warn('Usuario no autenticado. Redirigiendo a login.');
        this.redirigirLogin();
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

/* Estilos del slider de banners */
.banner-slider {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  margin-bottom: 20px;
  padding: 10px 0;
  scroll-snap-type: x mandatory;
}

.banner-slide {
  flex: 0 0 auto;
  width: 100%;
  max-width: 300px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  scroll-snap-align: center;
}

.banner-slide img {
  width: 100%;
  height: 200px;
  object-fit: cover;
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
  height: 200px;
  object-fit: cover;
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

/* Indicadores de carga */
p {
  font-size: 16px;
  color: #555;
  text-align: center;
  margin-top: 20px;
}
</style>
