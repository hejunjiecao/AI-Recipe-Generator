<template>
    <header class="header">
      <nav class="navbar">
        <div class="navbar-left">
          <a href="#" class="navbar-brand">aicooking</a>
        </div>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: 'Header'
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
  </style>