<template>
  <header class="header">
    <nav class="navbar">
      <div class="navbar-left">
        <a href="#" class="navbar-brand">aicooking</a>
      </div>
      <div class="navbar-right">
        <span class="style-label">Food Style:</span>
        <select v-model="selectedStyle" @change="updateStyle">
          <option value="Chinese">Chinese</option>
          <option value="German">German</option>
        </select>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      selectedStyle: 'Chinese' // Default value
    };
  },
  methods: {
    updateStyle() {
      this.$emit('style-changed', this.selectedStyle); 
    }
  }
};
</script>

<style scoped>
.header {
  width: 100%;
  background-color: #343a40;
  padding: 5px 15px;
  position: fixed;
  top: 0;
  z-index: 1000;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
}

.navbar-brand {
  font-size: 1.2em;
  color: #fff;
  text-decoration: none;
}

.navbar-brand:hover {
  color: #ddd;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.style-label {
  color: #fff;
  margin-right: 10px;
  font-size: 1em;
}

.navbar-right select {
  padding: 5px;
  border: none;
  background-color: #fff;
  color: #343a40;
  font-size: 1em;
}
</style>