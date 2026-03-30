<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Placeholder inputs
const name = ref('')
const temperature = ref('')
const mode = ref('')
</script>

<template>
<div class="flex flex-col h-screen bg-surface overflow-hidden">

  <!-- Header / Camera Placeholder -->
  <div class="flex justify-center mt-12 mb-8">

  </div>

  <!-- Form Inputs -->
  <main class="flex-1 px-6 space-y-6">
    <div class="flex flex-col space-y-2">
      <label class="font-headline text-xs tracking-widest uppercase text-on-surface/60 font-medium">Name</label>
      <input v-model="name" placeholder="Name"
             class="w-full px-4 py-3 rounded-lg border border-outline-variant/30 bg-white text-black"/>
    </div>

    <div class="flex flex-col space-y-2">
      <label class="font-headline text-xs tracking-widest uppercase text-on-surface/60 font-medium">Temperature</label>
      <input v-model="temperature" placeholder="Temperature"
             class="w-full px-4 py-3 rounded-lg border border-outline-variant/30 bg-white text-black"/>
    </div>

    <div class="flex flex-col space-y-2">
      <label class="font-headline text-xs tracking-widest uppercase text-on-surface/60 font-medium">Mode</label>
      <input v-model="mode" placeholder="Mode"
             class="w-full px-4 py-3 rounded-lg border border-outline-variant/30 bg-white text-black"/>
    </div>

    <button class="mt-6 w-full px-6 py-3 rounded-lg border-2 border-primary text-primary font-bold hover:bg-primary/10 transition">
      Save
    </button>
  </main>


</div>
</template>

<style scoped>
body { background-color: #0c0e17; color: #f0f0fd; font-family: 'Manrope', sans-serif; }
.material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
</style>