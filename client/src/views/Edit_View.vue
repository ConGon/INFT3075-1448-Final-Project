<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { store, addProfile } from './ProfileStore.js'

const API = 'http://localhost:8000'
const router = useRouter()
const route = useRoute()

const profiles = ref([])
const loading = ref(false)
const error = ref('')

async function fetchAgents() {
  try {
    const res = await fetch(`${API}/agents`)
    if (!res.ok) throw new Error('Failed to fetch agents')
    profiles.value = await res.json()
    // Update the store for dropdowns
    profiles.value.forEach(p => addProfile(p.name))
  } catch (err) {
    console.error(err)
    error.value = 'Failed to fetch agents.'
  }
}

onMounted(fetchAgents)

const isDetail = computed(() => !!route.params.id)
const currentProfile = computed(() => profiles.value.find(p => p.id === route.params.id))

function goToAdd() {
  router.push('/add')
}

async function saveProfile() {
  if (!currentProfile.value) return
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`${API}/agents/${currentProfile.value.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: currentProfile.value.name,
        personality: currentProfile.value.personality,
        instructions: currentProfile.value.instructions,
        task: currentProfile.value.task
      })
    })
    if (!res.ok) throw new Error('Failed to update agent')
    await fetchAgents()
    router.push('/') // Go back to list after save
  } catch (err) {
    console.error(err)
    error.value = 'Failed to save agent.'
  } finally {
    loading.value = false
  }
}

async function deleteProfile(id) {
  try {
    const res = await fetch(`${API}/agents/${id}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete agent')
    profiles.value = profiles.value.filter(p => p.id !== id)
    router.push('/')
  } catch (err) {
    console.error(err)
    error.value = 'Failed to delete agent.'
  }
}
</script>

<template>
<div class="flex flex-col h-screen bg-surface overflow-hidden pb-20 px-6 py-6">

  <header class="mb-6 flex justify-between items-center">
    <h1 class="text-lg font-bold">Agents</h1>
    <button @click="goToAdd"
      class="px-4 py-2 rounded-lg border border-outline-variant/30 text-on-surface hover:bg-on-surface/5 transition">
      Add New
    </button>
  </header>

  <div v-if="error" class="text-error mb-4">{{ error }}</div>

  <!-- LIST VIEW -->
  <div v-if="!isDetail" class="flex flex-col gap-4 overflow-y-auto">
    <div v-if="profiles.length === 0" class="text-on-surface/40 text-center mt-12 text-sm">
      No agents yet. Tap Add to create one.
    </div>
    <div v-for="profile in profiles" :key="profile.id" class="border p-4 rounded-lg flex justify-between items-center cursor-pointer hover:bg-on-surface/5"
         @click="router.push(`/edit/${profile.id}`)">
      <div>
        <div class="font-medium">{{ profile.name }}</div>
        <div class="text-xs text-on-surface/40 truncate">{{ profile.personality }}</div>
      </div>
      <span class="material-symbols-outlined text-on-surface/30">chevron_right</span>
    </div>
  </div>

  <!-- DETAIL VIEW -->
  <div v-else-if="currentProfile" class="flex flex-col gap-4 max-w-xs mx-auto">
    <button @click="router.push('/')" class="px-4 py-2 rounded-lg border border-outline-variant/30 hover:bg-on-surface/5">
      Back
    </button>

    <input v-model="currentProfile.name" placeholder="Name" class="px-4 py-2 border rounded-lg bg-white text-black"/>
    <input v-model="currentProfile.personality" placeholder="Personality" class="px-4 py-2 border rounded-lg bg-white text-black"/>
    <input v-model="currentProfile.instructions" placeholder="Instructions" class="px-4 py-2 border rounded-lg bg-white text-black"/>
    <input v-model="currentProfile.task" placeholder="Task" class="px-4 py-2 border rounded-lg bg-white text-black"/>

    <button @click="saveProfile" :disabled="loading"
      class="w-full px-6 py-3 mt-2 rounded-lg border-2 border-primary text-primary font-bold hover:bg-primary/10 transition disabled:opacity-50">
      {{ loading ? 'Saving...' : 'Save' }}
    </button>
    <button @click="deleteProfile(currentProfile.id)"
      class="w-full px-6 py-3 mt-2 rounded-lg border-2 border-error text-error font-bold hover:bg-error/10 transition">
      Delete
    </button>
  </div>
</div>
</template>

<style scoped>
body { background-color: #0c0e17; color: #f0f0fd; font-family: 'Manrope', sans-serif; }
.material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
</style>