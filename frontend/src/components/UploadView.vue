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
    <b-button
      pill
      id="upload-button"
      @click="uploadImage"
      variant="dark"
      :disabled="!file"
      class="mb-3"
    >
      Upload
    </b-button>
    <Recipe v-if="showRecipe" />
  </div>
</template>

<script>
import axios from 'axios';
import Recipe from './Recipe.vue';

export default {
  name: 'UploadView',
  components: {
    Recipe
  },
  data() {
    return {
      file: null,
      showRecipe: false,
    };
  },
  methods: {
    selectFile() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    uploadImage() {
      if (!this.file) return;

      const formData = new FormData();
      formData.append('file', this.file);

      axios.post('http://192.168.179.3:5008/uploads', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => {
		console.log(response.data.message);
        this.file = null;
        this.showRecipe = true;
      })
      .catch(err => {
        console.error(err);
      });
    },
  },
}
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

#select-button {
  width: 200px;
  margin-top: 20px;
}

#upload-button {
  width: 150px;
}
</style>
