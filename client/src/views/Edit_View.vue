<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Sample profiles (placeholder)
const profiles = ref([
  { id: 1, label: 'Profile 1', icon: 'play_arrow', width: 'w-32', temperature: '0.7', mode: 'Text Generation' },
  { id: 2, label: 'Profile 2', icon: 'circle', width: 'w-48', temperature: '0.5', mode: 'Text Generation' },
  { id: 3, label: 'Profile 3', icon: 'square', width: 'w-40', temperature: '1.0', mode: 'Text Generation' },
])

// Determine if viewing detail
const isDetail = computed(() => !!route.params.id)
const currentProfile = computed(() => profiles.value.find(p => p.id == route.params.id))

// Navigation
function goToProfile(id) {
  router.push(`/edit/${id}`)
}

function deleteProfile(id) {
  profiles.value = profiles.value.filter(p => p.id !== id)
  router.push('/edit') // back to list
}
</script>

<template>
<div class="flex flex-col h-screen bg-surface overflow-hidden">

  <!-- LIST VIEW -->
  <main v-if="!isDetail" class="flex-1 overflow-y-auto px-6 space-y-4 pt-6">
    <div
      v-for="profile in profiles"
      :key="profile.id"
      @click="goToProfile(profile.id)"
      class="border border-outline-variant/30 rounded-xl p-4 flex items-center gap-4 cursor-pointer active:scale-95 transition"
    >
      <div class="w-8 h-8 rounded border border-outline-variant/30 flex items-center justify-center">
        <span class="material-symbols-outlined text-sm opacity-50">{{ profile.icon }}</span>
      </div>
      <div :class="['h-2 bg-outline-variant/20 rounded-full', profile.width]"></div>
      <div class="ml-2 text-on-surface">{{ profile.label }}</div>
    </div>
  </main>

  <!-- DETAIL VIEW -->
  <main v-else class="flex flex-col flex-1 overflow-y-auto p-6 pt-24">
    <!-- Back button fixed at top -->
    <header class="fixed top-0 left-0 w-full bg-surface border-b border-outline-variant/20 px-6 py-4 z-50 flex items-center">
      <button
        @click="router.push('/edit')"
        class="px-4 py-2 rounded-lg border border-outline-variant/30 text-on-surface hover:bg-on-surface/5 transition"
      >
        Back
      </button>
    </header>

    <!-- Spacer for fixed header -->
    <div class="h-16"></div>

    <div class="flex flex-col items-center gap-6">
      <div class="text-on-surface font-bold text-xl mb-2">{{ currentProfile.label }}</div>

      <!-- Icon preview -->
      <div class="w-32 h-32 rounded-full bg-surface-container-high flex items-center justify-center">
        <span class="material-symbols-outlined text-4xl">{{ currentProfile.icon }}</span>
      </div>

      <!-- Editable fields -->
      <input v-model="currentProfile.label" placeholder="Name"
             class="w-full max-w-xs px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>

      <input v-model="currentProfile.temperature" placeholder="Temperature"
             class="w-full max-w-xs px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>

      <input v-model="currentProfile.mode" placeholder="Mode"
             class="w-full max-w-xs px-4 py-2 rounded-lg border border-outline-variant/30 bg-white text-black"/>

      <button
        class="mt-4 px-6 py-3 rounded-lg border-2 border-primary text-primary font-bold hover:bg-primary/10 transition"
      >
        Save
      </button>

      <button
        @click="deleteProfile(currentProfile.id)"
        class="mt-2 px-6 py-3 rounded-lg border-2 border-error text-error font-bold hover:bg-error/10 transition"
      >
        Delete
      </button>
    </div>
  </main>

</div>
</template>

<style scoped>
body { background-color: #0c0e17; color: #f0f0fd; font-family: 'Manrope', sans-serif; }
.material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
</style>