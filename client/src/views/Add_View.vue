<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { addProfile } from './ProfileStore.js'

const router = useRouter()
const name = ref('')
const personality = ref('')
const instructions = ref('')
const task = ref('')
const loading = ref(false)
const error = ref('')

async function addAgent() {
  if (!name.value || !personality.value || !instructions.value || !task.value) {
    error.value = 'All fields are required.'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const res = await fetch('http://localhost:8000/agents', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name.value,
        personality: personality.value,
        instructions: instructions.value,
        task: task.value
      })
    })
    if (!res.ok) throw new Error('Failed to add agent')
    
    // Add to local store so dropdown updates immediately
    addProfile(name.value)
    router.push('/') // Return to list
  } catch (err) {
    console.error(err)
    error.value = 'Failed to add agent.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
<div class="flex flex-col h-screen bg-surface overflow-hidden px-6 py-6">

  <header class="mb-6">
    <button @click="router.push('/')"
      class="px-4 py-2 rounded-lg border border-outline-variant/30 text-on-surface hover:bg-on-surface/5 transition">
      Back
    </button>
  </header>

  <div class="flex flex-col gap-4 max-w-xs mx-auto">
    <div v-if="error" class="text-error">{{ error }}</div>

    <input v-model="name" placeholder="Name"
      class="px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>
    <input v-model="personality" placeholder="Personality"
      class="px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>
    <input v-model="instructions" placeholder="Instructions"
      class="px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>
    <input v-model="task" placeholder="Task"
      class="px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>

    <button @click="addAgent" :disabled="loading"
      class="mt-4 w-full px-6 py-3 rounded-lg border-2 border-primary text-primary font-bold hover:bg-primary/10 transition disabled:opacity-50">
      {{ loading ? 'Saving...' : 'Save' }}
    </button>
  </div>
</div>
</template>

<style scoped>
body { background-color: #0c0e17; color: #f0f0fd; font-family: 'Manrope', sans-serif; }
</style>