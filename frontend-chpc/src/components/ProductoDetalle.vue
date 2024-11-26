<template>
    <div class="producto-container">
      <!-- Mensaje de carga -->
      <div v-if="isLoading" class="loading-message">
        <p>Cargando detalles del producto...</p>
      </div>
  
      <!-- Mensaje de error con botón de recarga -->
      <div v-if="errorMessage && !isLoading" class="error-message">
        <p>{{ errorMessage }}</p>
        <button @click="recargarProducto">Reintentar</button>
      </div>
  
      <!-- Detalles del producto -->
      <div v-if="producto && !isLoading && !errorMessage" class="producto-detalle">
        <!-- Imágenes del producto -->
        <div class="producto-imagenes">
          <img
            v-for="(visual, index) in producto.visuales"
            :key="index"
            :src="visual.url"
            :alt="`Imagen del producto ${producto.nombre}`"
            class="imagen-pequena"
          />
        </div>
  
        <!-- Información del producto -->
        <div class="producto-informacion">
          <h1 class="producto-nombre">{{ producto.nombre }}</h1>
          <p class="producto-precio">Precio: ${{ formatPrice(producto.precio) }}</p>
          <p class="producto-stock">{{ producto.stock > 0 ? "Disponible" : "Agotado" }}</p>
          <p><strong>Categoría:</strong> {{ producto.categoria?.nombre || 'Sin categoría' }}</p>
  
          <p v-if="producto.peso"><strong>Peso:</strong> {{ producto.peso }} kg</p>
          <p v-if="producto.color"><strong>Color:</strong> {{ producto.color }}</p>
          <p v-if="producto.tamaño"><strong>Tamaño:</strong> {{ producto.tamaño }}</p>
  
          <button class="boton-carrito">Añadir al carrito</button>
        </div>
  
        <!-- Reseñas del producto -->
        <div class="producto-reseñas">
          <h3>Reseñas</h3>
          <div v-if="producto.reseñas?.length">
            <div v-for="(reseña, index) in producto.reseñas" :key="index" class="reseña">
              <p><strong>Usuario:</strong> {{ reseña.usuario }}</p>
              <p><strong>Calificación:</strong> {{ reseña.calificacion }} / 5</p>
              <p><strong>Comentario:</strong> {{ reseña.comentario }}</p>
              <p><small>{{ formatDate(reseña.fecha) }}</small></p>
            </div>
          </div>
          <div v-else>
            <p>No hay reseñas para este producto.</p>
          </div>
  
          <!-- Formulario para agregar una reseña -->
          <div class="agregar-reseña">
            <h3>Agregar una reseña</h3>
            <form @submit.prevent="enviarReseña">
              <label for="calificacion">Calificación:</label>
              <select v-model="nuevaReseña.calificacion" id="calificacion" required>
                <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
              </select>
  
              <label for="comentario">Comentario:</label>
              <textarea v-model="nuevaReseña.comentario" id="comentario" rows="3" required></textarea>
  
              <button type="submit" class="boton-reseña">Enviar Reseña</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        producto: null,
        errorMessage: "",
        isLoading: true,
        nuevaReseña: {
          calificacion: null,
          comentario: "",
        },
      };
    },
    methods: {
      async cargarProducto() {
        this.isLoading = true;
        this.errorMessage = "";
  
        const productoId = this.$route.params.id;
        try {
          const response = await axios.get(`http://localhost:5000/tienda/productos/${productoId}`);
          if (response.data.status === "success") {
            this.producto = response.data.data;
          } else {
            this.errorMessage = response.data.message || "Error al cargar el producto.";
          }
        } catch (error) {
          this.errorMessage = error.response?.data?.message || "Hubo un problema al cargar el producto. Intenta de nuevo más tarde.";
        } finally {
          this.isLoading = false;
        }
      },
      async enviarReseña() {
        const productoId = this.$route.params.id;
        try {
          const response = await axios.post(`http://localhost:5000/tienda/productos/${productoId}/reseñas`, {
            usuario_id: 1, // Cambia esto por el ID real del usuario autenticado
            calificación: this.nuevaReseña.calificacion,
            comentario: this.nuevaReseña.comentario,
          });
  
          if (response.data.status === "success") {
            this.producto.reseñas.push(response.data.data);
            this.nuevaReseña = { calificacion: null, comentario: "" };
          } else {
            this.errorMessage = response.data.message || "Error al enviar la reseña.";
          }
        } catch (error) {
          this.errorMessage = error.response?.data?.message || "Hubo un problema al enviar la reseña. Intenta de nuevo más tarde.";
        }
      },
      recargarProducto() {
        this.cargarProducto();
      },
      formatPrice(price) {
        return parseFloat(price).toFixed(2);
      },
      formatDate(date) {
        return new Date(date).toLocaleDateString("es-ES", {
          year: "numeric",
          month: "long",
          day: "numeric",
        });
      },
    },
    created() {
      this.cargarProducto();
    },
  };
  </script>
  
  <style scoped>
  
  .producto-container {
    display: flex;
    max-width: 1200px;
    margin: auto;
    padding: 20px;
    gap: 20px;
  }
  
  .producto-imagenes {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .imagen-pequena {
    width: 100%;
    max-width: 200px;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
  }
  
  .imagen-pequena:hover {
    transform: scale(1.1);
  }
  
  .producto-informacion {
    flex: 2;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .producto-nombre {
    font-size: 24px;
    font-weight: bold;
  }
  
  .producto-precio {
    font-size: 22px;
    color: #ff6600;
    font-weight: bold;
  }
  
  .producto-stock {
    font-size: 16px;
    color: green;
  }
  
  .boton-carrito {
    background-color: #ff6600;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: background-color 0.3s ease;
  }
  
  .boton-carrito:hover {
    background-color: #e55b00;
  }
  
  .producto-reseñas {
    margin-top: 20px;
  }
  
  .reseña {
    border: 1px solid #ddd;
    padding: 15px;
    margin-top: 10px;
    border-radius: 5px;
    background-color: #f9f9f9;
  }
  
  .agregar-reseña {
    margin-top: 20px;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    background-color: #f3f3f3;
  }
  
  .boton-reseña {
    background-color: #007bff;
    color: white;
    padding: 8px 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s ease;
  }
  
  .boton-reseña:hover {
    background-color: #0056b3;
  }
  
  .loading-message,
  .error-message {
    text-align: center;
    font-size: 18px;
    margin-top: 50px;
  }
  
  .error-message {
    color: red;
  }
  
  .error-message button {
    background-color: #ff9900;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 10px;
    transition: background-color 0.3s ease;
  }
  
  .error-message button:hover {
    background-color: #ff8c00;
  }
  </style>
  