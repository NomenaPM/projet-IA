<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
    <div class="w-full max-w-3xl bg-white shadow-lg rounded-lg overflow-hidden">
      <!-- Header with wavy border -->
      <div class="bg-yellow-300 p-4 relative">
        <div class="flex items-center gap-2">
          <!-- Owl Logo -->
          <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center overflow-hidden">
            <div class="flex items-center space-x-1">
              <div class="w-2.5 h-2.5 bg-gray-600 rounded-full"></div>
              <div class="w-2.5 h-2.5 bg-gray-600 rounded-full"></div>
            </div>
          </div>
          <h1 class="font-bold text-gray-800 tracking-wide uppercase text-2xl">Image Recognition</h1>
        </div>
        <!-- Wavy border -->
        <div class="absolute -bottom-1 left-0 right-0">
          <svg viewBox="0 0 1200 120" preserveAspectRatio="none" class="w-full h-6 text-white fill-current">
            <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z"></path>
          </svg>
        </div>
      </div>

      <!-- Main Content -->
      <div class="p-6 relative">
        <!-- Background dots pattern -->
        <div class="absolute inset-0 opacity-5">
          <div class="grid grid-cols-12 gap-3">
            <div v-for="n in 144" :key="n" class="w-1.5 h-1.5 bg-gray-400 rounded-full"></div>
          </div>
        </div>

        <!-- Content -->
        <div class="relative">
          <h2 class="text-2xl font-bold mb-4 text-center">Upload an Image</h2>
          <div class="flex justify-center mb-4">
            <label 
              for="image-upload"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer focus:outline-none focus:shadow-outline"
            >
              Select Image
              <input
                type="file"
                id="image-upload"
                @change="handleFileUpload"
                accept="image/*"
                class="hidden"
              />
            </label>
          </div>
          <button 
            @click="uploadImage"
            class="w-full bg-yellow-400 hover:bg-yellow-500 text-gray-800 font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          >
            Upload
          </button>

          <div v-if="imageUrl" class="mt-8">
            <h3 class="text-xl font-bold mb-4">Recognition Result</h3>
            <div class="flex items-center justify-center mb-4">
              <img :src="imageUrl" alt="Uploaded Image" class="max-w-full h-auto max-h-48 rounded-lg shadow-md" />
            </div>
            <p class="mb-4"><strong>Model Response:</strong> {{ modelResponse }}</p>
        
            <audio v-if="audioUrl" :src="audioUrl" controls @error="handleAudioError"></audio>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedFile = ref(null)
const imageUrl = ref(null)
const modelResponse = ref('')
const audioUrl = ref('')
const audioPlayer = ref(null)

const handleFileUpload = (event) => {
  selectedFile.value = event.target.files[0]
  imageUrl.value = URL.createObjectURL(selectedFile.value)
}

const uploadImage = async () => {
  if (!selectedFile.value) {
    alert("Please select an image to upload.");
    return;
  }
  
  const formData = new FormData();
  formData.append("file", selectedFile.value);
  
  try {
    const response = await axios.post("http://127.0.0.1:5000/pictures", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    
    modelResponse.value = response.data.model_response;
    audioUrl.value = response.data.audio_file_url;

    // Play the audio if the URL is available
    if (response.data.audio_file_url) {
        audioUrl.value = response.data.audio_file_url;

    const audio = new Audio(audioUrl.value);
        audio.play().catch((playError) => {
        console.error("Error playing audio:", playError);
    });
    } else {
        console.warn("No audio file URL returned.");
}   

  } catch (error) {
    console.error("Error uploading image:", error);
    alert("There was an error processing the image.");
  }
};


</script>