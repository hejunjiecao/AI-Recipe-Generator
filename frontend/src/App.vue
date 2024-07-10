<template>
  <div id="app">
    <Header @style-changed="handleStyleChange" />
    <main class="main-content">
      <upload-view :selected-style="selectedStyle" />
    </main>
  </div>
</template>

<script>
import Header from './components/Header.vue';
import UploadView from './components/UploadView.vue';

export default {
  name: 'App',
  components: {
    Header,
    UploadView
  },
  data() {
    return {
      selectedStyle: 'Chinese'
    };
  },
  methods: {
    handleStyleChange(newStyle) {
      this.selectedStyle = newStyle;
    },
    updateTitle() {
      document.title = 'aicooking'; 
    }
  },
  mounted() {
    this.updateTitle();
  }
};
</script>

<style>
/* 全局样式 */
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.main-content {
  padding: 20px;
  padding-top: 80px;
  background-color: #f8f9fa;
}
</style>