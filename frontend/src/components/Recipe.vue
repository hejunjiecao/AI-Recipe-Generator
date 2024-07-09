<template>
  <div class="recipe" v-if="recipe">
    <div class="recipe-header">
      <h2 class="recipe-name">{{ recipe.dishName }}</h2>
      <p class="recipe-time">Total Time: {{ recipe.timeToPrepare }}</p>
    </div>
    <div class="recipe-body">
      <div class="ingredients">
        <h3>Ingredients</h3>
        <div class="ingredients-grid">
          <div class="ingredient-item" v-for="(amount, ingredient) in recipe.ingredients" :key="ingredient">
            {{ ingredient }}: {{ amount }}
          </div>
        </div>
      </div>
      <div class="steps">
        <h3>Steps</h3>
        <ol>
          <li v-for="(step, index) in recipe.Steps" :key="index">
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

.recipe-body {
  display: flex;
  flex-direction: column;
}

.ingredients {
  margin-bottom: 20px;
}

.ingredients-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.ingredient-item {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
}

.steps {
  margin-bottom: 20px;
}

ol {
  list-style: decimal inside;
  padding: 0;
  margin: 0;
}
</style>