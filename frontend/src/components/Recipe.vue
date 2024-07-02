<template>
  <div class="recipe" v-if="recipe">
    <div class="recipe-header">
      <h2 class="recipe-name">{{ recipe.dishName }}</h2>
      <p class="recipe-time">Total Time: {{ recipe.timeToPrepare }}</p>
    </div>
    <div class="recipe-body">
      <div class="ingredients">
        <h3>Ingredients</h3>
        <ul>
          <li v-for="(ingredient, index) in recipe.ingredients" :key="index">
            {{ ingredient.name }}: <strong>{{ ingredient.amount }}</strong>
          </li>
        </ul>
      </div>
      <div class="steps">
        <h3>Steps</h3>
        <ol>
          <li v-for="(step, index) in recipe.steps" :key="index">
            {{ step }}
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Recipe',
  props: {
    recipe: {
      type: Object,
      required: true
    }
  }
};
</script>

<style scoped>
.recipe {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  width: 100%;
  margin-top: 10px; 
}

.recipe-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.recipe-name {
  font-size: 2em;
  font-weight: bold;
}

.recipe-time {
  font-size: 1em;
  color: #999;
}

.ingredients, .steps {
  margin-bottom: 20px;
}

h3 {
  font-size: 1.5em;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

ul li::before {
  content: '•';
  color: #007BFF;
  font-weight: bold;
  display: inline-block;
  width: 1em;
  margin-left: -1em;
}

ol {
  list-style: decimal inside;
  padding: 0;
}

.pagination-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  width: 200px;
}
</style>