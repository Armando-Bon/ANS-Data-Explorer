<template>
  <div class="search-container">
    <h1>Busca de Operadoras</h1>
    
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchQuery" 
        @input="debounceSearch"
        placeholder="Digite sua busca..."
        class="search-input"
      >
    </div>
    
    <div v-if="loading" class="loading">
      Buscando...
    </div>
    
    <div v-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-if="results && results.length > 0" class="results">
      <h3>Resultados encontrados: {{ results.length }}</h3>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th v-for="(value, key) in results[0]" :key="key">
                {{ key }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(result, index) in results" :key="index">
              <td v-for="(value, key) in result" :key="key">
                {{ value || '-' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-if="!loading && !error && (!results || results.length === 0) && searchQuery" class="no-results">
      Nenhum resultado encontrado.
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'ProcurarComponente',
  setup() {
    const searchQuery = ref('')
    const results = ref([])
    const loading = ref(false)
    const error = ref(null)
    let searchTimeout = null

    const performSearch = async () => {
      if (!searchQuery.value) {
        results.value = []
        return
      }

      loading.value = true
      error.value = null
      console.log('Iniciando busca com query:', searchQuery.value)

      try {
        const url = `http://localhost:5001/api/search?q=${encodeURIComponent(searchQuery.value)}`
        console.log('Fazendo requisição para:', url)
        
        const response = await axios.get(url)
        console.log('Resposta recebida:', response.data)
        
        if (response.data.error) {
          throw new Error(response.data.error)
        }
        
        const searchResults = Array.isArray(response.data.results) ? response.data.results : []
        results.value = searchResults
        
        console.log('Resultados processados:', results.value.length)
        if (results.value.length > 0) {
          console.log('Primeiro resultado:', results.value[0])
        }
      } catch (err) {
        console.error('Erro detalhado:', err)
        error.value = err.response?.data?.error || 'Erro ao realizar a busca. Por favor, tente novamente.'
        results.value = []
      } finally {
        loading.value = false
      }
    }

    const debounceSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(performSearch, 300)
    }

    return {
      searchQuery,
      results,
      loading,
      error,
      debounceSearch
    }
  }
}
</script>

<style scoped>
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-box {
  margin: 20px 0;
}

.search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 6px;
  outline: none;
}

.search-input:focus {
  border-color: #4CAF50;
}

.loading {
  text-align: center;
  color: #666;
  margin: 20px 0;
}

.error {
  color: #ff0000;
  text-align: center;
  margin: 20px 0;
}

.no-results {
  text-align: center;
  color: #666;
  margin: 20px 0;
}

.results {
  margin-top: 20px;
}

.results h3 {
  margin-bottom: 15px;
  color: #333;
}

.table-container {
  overflow-x: auto;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  white-space: nowrap;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 1;
}

tr:hover {
  background-color: #f9f9f9;
}

td {
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style> 