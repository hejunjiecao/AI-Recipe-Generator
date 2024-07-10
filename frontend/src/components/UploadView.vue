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

    <!-- 加载按钮 -->
    <div v-if="isLoading" class="loader"></div>

    <div v-if="showIngredients" class="ingredients-container">
      <div v-for="(ingredient, index) in ingredients" :key="index" class="ingredient-button">
        <button class="ingredient">{{ ingredient }}</button>
        <button class="remove-button" @click="removeIngredient(index)">×</button>
      </div>
      <button v-if="ingredients.length > 0" class="add-button" @click="addIngredient">+</button>
    </div>

    <div v-if="showRecipe">
      <Recipe :recipe="recipes[currentRecipeIndex]" />
      <div v-if="isRecipeLoaded" class="pagination-buttons">
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
      showIngredients: true,
      recipes: [],
      currentRecipeIndex: 0,
      isLoading: false, // 加载状态
      isRecipeLoaded: false // Recipe加载状态
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

      this.isLoading = true; // 开始加载

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await axios.post('http://localhost:5008/uploads', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log(response.data.message);
        let ingredientsData = response.data.ingredients;
        if (typeof ingredientsData === 'string') {
          const match = ingredientsData.match(/\[.*\]/);
          if (match) {
            ingredientsData = JSON.parse(match[0]);
          } else {
            console.error('Failed to parse ingredients:', ingredientsData);
          }
        }
        this.ingredients = ingredientsData;
        this.file = null;
        this.showRecipe = false;
        this.showIngredients = true;
      } catch (error) {
        console.error('Error uploading file:', error);
      } finally {
        this.isLoading = false; // 结束加载
      }
    },
    async generateRecipe() {
      this.isLoading = true; // 开始加载
      this.isRecipeLoaded = false; // 还未加载recipe

      this.showIngredients = false;
      this.showRecipe = true;
      const style = this.selectedStyle;
      const data = {
        style: style,
        ingredients: this.ingredients
      };
      try {
        const response = await axios.post('http://localhost:5008/generate', data, {
          headers: {
            'Content-Type': 'application/json',
          },
        });
        this.recipes = response.data.recipes;
        this.isRecipeLoaded = true; // recipe加载完成
      } catch (error) {
        console.error('Error generating recipe:', error);
      } finally {
        this.isLoading = false; // 结束加载
      }
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
/* 调整加载按钮尺寸 */
.loader {
  border: 4px solid #f3f3f3;
  border-radius: 50%;
  border-top: 4px solid #3498db;
  width: 30px;  /* 调整宽度 */
  height: 30px; /* 调整高度 */
  animation: spin 2s linear infinite;
  margin-top: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}


.ingredient {
  background-color: #6aa84f;
  color: white;
  border: none;
  padding: 10px;
  width: 150px; 
  height: 40px;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap; 
}


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