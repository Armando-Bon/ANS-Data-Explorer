<template>
  <div id="app">
    <ProcurarComponente />
  </div>
</template>

<script>
import ProcurarComponente from './components/ProcurarComponente.vue'

export default {
  name: 'App',
  components: {
    ProcurarComponente
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style> 