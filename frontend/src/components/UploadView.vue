<template>
  <div id="upload" class="d-flex flex-column align-items-center">
    <h3>Upload an Image</h3>
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
    >
      Upload
    </b-button>
    <div v-if="uploadMessage" class="result mt-3">
      <h4>{{ uploadMessage }}</h4>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      uploadMessage: '',
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

      axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      .then(response => {
        this.uploadMessage = response.data.message;
        this.file = null; // 重置文件选择
      })
      .catch(err => {
        console.error(err);
        this.uploadMessage = 'Failed to upload image';
      });
    },
  },
}
</script>

<style>
#upload {
  font-family: 'Lato', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh; /* 垂直居中 */
  background-color: #f8f9fa; /* 浅灰色背景 */
}

#upload h3 {
  margin-bottom: 20px;
}

#file-input {
  display: none; /* 隐藏文件输入框 */
}

#select-button {
  width: 200px; /* 固定宽度 */
}

#upload-button {
  width: 150px; /* 固定宽度 */
}

.result {
  margin-top: 20px;
  text-align: center;
  color: #28a745; /* 成功消息的绿色 */
}

#error-message {
  color: #dc3545; /* 错误消息的红色 */
}
</style>