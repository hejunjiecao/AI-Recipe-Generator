<template>
  <div id="upload" class="d-flex flex-column align-items-center">
    <input
      type="file"
      id="file-input"
      ref="fileInput"
      @change="handleFileChange"
      accept="image/*"
      capture="environment"
      style="display: none;"
    />
    <b-button pill id="select-button" @click="selectFile" variant="primary" class="mb-3">
      Take a Picture
    </b-button>

    <b-button pill id="generate-button" @click="generateRecipe" variant="dark" class="mb-3">
      Generate
    </b-button>

    <div v-if="showIngredients" class="ingredients-container">
      <div v-for="(ingredient, index) in ingredients" :key="index" class="ingredient-button">
        <button class="ingredient">{{ ingredient }}</button>
        <button class="remove-button" @click="removeIngredient(index)">×</button>
      </div>
      <button v-if="ingredients.length > 0" class="add-button" @click="addIngredient">+</button>
    </div>

    <div v-if="showRecipe">
      <Recipe :recipe="recipes[currentRecipeIndex]" />
      <div class="pagination-buttons">
        <button @click="prevRecipe" :disabled="currentRecipeIndex === 0">Previous</button>
        <button @click="nextRecipe" :disabled="currentRecipeIndex === recipes.length - 1">Next</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Recipe from '@/components/Recipe.vue';

export default {
  name: 'UploadView',
  components: {
    Recipe
  },
  props: {
    selectedStyle: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      file: null,
      showRecipe: false,
      ingredients: [],
    //   ingredients: ['tomato', 'cheese', 'bread', 'lettuce', 'chicken'],
      showIngredients: true,
      recipes: [],
      currentRecipeIndex: 0
    };
  },
  methods: {
    selectFile() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      this.file = event.target.files[0];
      this.uploadImage();
    },
    async uploadImage() {
      if (!this.file) return;

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await axios.post('http://localhost:5008/uploads', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response.data.message);
        this.ingredients = JSON.parse(response.data.message);
        this.file = null;
        this.showIngredients = true;
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
    async generateRecipe() {
      this.showIngredients = false;
      this.showRecipe = true;
    //   发送style和ingredients到后端
      const style = this.selectedStyle;
      const data = {
        style: style,
        ingredients: this.ingredients
      };
    //    请求后端recipe
      try {
        const response = await axios.post('http://localhost:5008/generate', data, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        this.recipes = response.data.recipes;
      } catch (error) {
        console.error('Error generating recipe:', error);
      }
//       this.recipes = [
//     {
//       dishName: 'Spaghetti Carbonara',
//       timeToPrepare: '30 minutes',
//       ingredients: [
//         { name: 'Spaghetti', amount: '200g' },
//         { name: 'Eggs', amount: '2' },
//         { name: 'Pancetta', amount: '100g' },
//         { name: 'Parmesan cheese', amount: '50g' },
//         { name: 'Black pepper', amount: 'to taste' }
//       ],
//       steps: [
//         'Boil the spaghetti.',
//         'Fry the pancetta.',
//         'Mix eggs and cheese.',
//         'Combine everything with spaghetti.',
//         'Season with black pepper.'
//       ]
//     },
//     {
//       dishName: 'Chicken Alfredo',
//       timeToPrepare: '40 minutes',
//       ingredients: [
//         { name: 'Fettuccine', amount: '200g' },
//         { name: 'Chicken breast', amount: '2' },
//         { name: 'Heavy cream', amount: '1 cup' },
//         { name: 'Parmesan cheese', amount: '50g' },
//         { name: 'Garlic', amount: '2 cloves' }
//       ],
//       steps: [
//         'Cook the fettuccine.',
//         'Sauté the chicken.',
//         'Prepare the Alfredo sauce.',
//         'Combine pasta and sauce.',
//         'Serve with grated Parmesan.'
//       ]
//     },
//     {
//       dishName: 'Beef Stir Fry',
//       timeToPrepare: '25 minutes',
//       ingredients: [
//         { name: 'Beef', amount: '300g' },
//         { name: 'Broccoli', amount: '1 head' },
//         { name: 'Soy sauce', amount: '1/4 cup' },
//         { name: 'Garlic', amount: '3 cloves' },
//         { name: 'Ginger', amount: '1 inch' }
//       ],
//       steps: [
//         'Slice the beef.',
//         'Chop the broccoli.',
//         'Stir fry beef and broccoli.',
//         'Add soy sauce, garlic, and ginger.',
//         'Serve with rice.'
//       ]
//     }

//   ];
    },
    nextRecipe() {
      if (this.currentRecipeIndex < this.recipes.length - 1) {
        this.currentRecipeIndex++;
      }
    },
    prevRecipe() {
      if (this.currentRecipeIndex > 0) {
        this.currentRecipeIndex--;
      }
    },
    addIngredient() {
      if (this.ingredients.length < 16) {
        const newIngredient = prompt("Enter a new ingredient:");
        if (newIngredient) {
          this.ingredients.push(newIngredient);
        }
      }
    },
    removeIngredient(index) {
      this.ingredients.splice(index, 1);
    }
  }
};
</script>

<style>
html, body, #upload {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Lato', sans-serif;
  background-color: #f8f9fa;
}

#upload {
  color: #2c3e50;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

#select-button, #generate-button {
  width: 200px;
  margin-top: 20px;
}

.ingredients-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 20px;
}

.ingredient-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ingredient {
  background-color: #6aa84f;
  color: white;
  border: none;
  padding: 10px;
  width: 100px;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.remove-button {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: red;
  color: white;
  border: none;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-button {
  background-color: green;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.pagination-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  width: 200px;
}
</style>
