<template>
  <div class="relative h-screen flex items-center justify-center bg-[#0c0e17]">

    <!-- Settings Drawer -->
    <div class="settings-drawer fixed top-0 left-0 w-full z-[60] bg-[#11131d] flex flex-col" id="settings-drawer">
      <div class="flex-1 p-8 flex flex-col justify-center space-y-4">

        <!-- Agent Dropdown -->
        <div class="p-6 rounded-xl border border-outline-variant/30 bg-[#1c1f2b]">
          <label class="font-headline font-bold tracking-widest text-on-surface text-lg block mb-2">
            AGENT
          </label>
          <select v-model="selectedAgent" class="w-full px-3 py-2 rounded bg-[#0c0e17] text-on-surface">
            <option v-for="agent in agents" :key="agent.id" :value="agent.id">
              {{ agent.name }}
            </option>
          </select>
        </div>

        <!-- Prompt Input -->
        <div class="p-6 rounded-xl border border-outline-variant/30 bg-[#1c1f2b]">
          <label class="font-headline font-bold tracking-widest text-on-surface text-lg block mb-2">
            PROMPT
          </label>
          <input
            v-model="userPrompt"
            type="text"
            placeholder="Type your prompt here..."
            class="w-full px-3 py-2 rounded bg-[#0c0e17] text-on-surface focus:outline-none focus:ring-2 focus:ring-purple-500"
            @keyup.enter="updateAI"
          />
        </div>

        <!-- Temperature Input -->
        <div class="p-6 rounded-xl border border-outline-variant/30 bg-[#1c1f2b]">
          <label class="font-headline font-bold tracking-widest text-on-surface text-lg block mb-2">
            TEMPERATURE
          </label>
          <input
            v-model="temperature"
            type="number"
            min="0"
            max="1"
            step="0.1"
            placeholder="0.5"
            class="w-full px-3 py-2 rounded bg-[#0c0e17] text-on-surface focus:outline-none focus:ring-2 focus:ring-purple-500"
          />
        </div>

        <!-- Ask Button -->
        <button
          @click="updateAI"
          :disabled="loading || !selectedAgent || !userPrompt"
          class="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-30 disabled:cursor-not-allowed text-white font-bold tracking-widest text-sm uppercase transition-all duration-200"
        >
          {{ loading ? 'Thinking...' : 'Ask' }}
        </button>

      </div>

      <!-- Drawer Handle -->
      <div class="settings-handle" @click="toggleSettings">
        <span class="material-symbols-outlined text-outline transition-transform duration-500" id="handle-icon">
          expand_more
        </span>
      </div>
    </div>

    <!-- Crystal Ball -->
    <div class="crystal-ball animate-float relative z-10">
      <div class="inner-glow"></div>

      <!-- Loading spinner -->
      <div v-if="loading" class="loading-ring"></div>

      <!-- AI Text -->
      <div
        v-else
        ref="aiTextRef"
        class="ai-output text-center text-purple-400 font-bold"
      >
        <template v-if="aiText">
          <template v-for="(line, index) in formattedLines" :key="index">
            <div>{{ line }}</div>
          </template>
        </template>
        <span v-else class="text-white/20 text-sm font-normal">awaiting query…</span>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { store, setAgents, setProfiles } from './ProfileStore.js'

const selectedProfile = ref('')
const selectedAgent = ref('')
const userPrompt = ref('')
const temperature = ref(0.5)
const loading = ref(false)

const profiles = computed(() => store.profiles)
const agents = computed(() => store.agents)

// Fetch agents from backend
async function fetchData() {
  try {
    const res = await fetch('http://localhost:8000/agents')
    const data = await res.json()
    setAgents(data)
    setProfiles(data.map(a => ({ id: a.id, name: a.name })))
  } catch (err) {
    console.error('Fetch failed:', err)
  }
}

onMounted(fetchData)

// AI Crystal Ball
const aiText = ref('')
const aiTextRef = ref(null)

async function updateAI() {
  if (!selectedAgent.value || !userPrompt.value) return
  const agent = store.agents.find(a => a.id === selectedAgent.value)
  if (!agent) return
  loading.value = true
  try {
    const res = await fetch('http://localhost:8000/run-agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personality: agent.personality || agent.name,
        instructions: agent.instructions || '',
        task: userPrompt.value,
        temperature: temperature.value
      })
    })
    const data = await res.json()
    aiText.value = data.result
  } catch (err) {
    aiText.value = 'Error contacting AI'
  } finally {
    loading.value = false
  }
}

// Fit font inside crystal ball
function fitFont() {
  nextTick(() => {
    if (!aiTextRef.value) return
    let currentFontSize = 20
    aiTextRef.value.style.fontSize = currentFontSize + 'px'
    while (
      aiTextRef.value.scrollWidth > aiTextRef.value.clientWidth &&
      currentFontSize > 14
    ) {
      currentFontSize -= 1
      aiTextRef.value.style.fontSize = currentFontSize + 'px'
    }
  })
}

watch(aiText, fitFont)
onMounted(fitFont)

function toggleSettings() {
  const drawer = document.getElementById('settings-drawer')
  const icon = document.getElementById('handle-icon')
  const isOpen = drawer.classList.toggle('is-open')
  icon.style.transform = isOpen ? 'rotate(180deg)' : 'rotate(0deg)'
}

const formattedLines = computed(() => {
  if (!aiText.value) return []
  const words = aiText.value.split(' ')
  const lines = []
  let currentLine = []
  words.forEach(word => {
    currentLine.push(word)
    if (currentLine.join(' ').length > 10) {
      lines.push(currentLine.join(' '))
      currentLine = []
    }
  })
  if (currentLine.length) lines.push(currentLine.join(' '))
  return lines.map((line, i) => {
    const pad = Math.abs(Math.floor(lines.length / 2) - i)
    return ' '.repeat(pad * 2) + line
  })
})
</script>

<style scoped>
.ai-output {
  position: relative;
  width: 75%;
  height: 75%;
  overflow-x: hidden;
  line-height: 1.2; 
  scrollbar-width: none;
}
.settings-drawer {
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(calc(-100% + 48px)); /* FIX: spaces around + */
}
.settings-drawer.is-open { transform: translateY(0); }
.settings-handle { height:48px; display:flex; align-items:center; justify-content:center; cursor:pointer; }

.crystal-ball {
  width:500px; height:500px; border-radius:50%;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15), rgba(255,255,255,0) 70%),
              radial-gradient(circle at 50% 50%, rgba(126,81,255,0.1), rgba(0,227,253,0.05));
  box-shadow: inset 0 0 50px rgba(126,81,255,0.2), inset 0 0 20px rgba(0,227,253,0.2), 0 0 60px rgba(126,81,255,0.1), 0 0 100px rgba(0,227,253,0.05);
  display:flex; align-items:center; justify-content:center; border:1px solid rgba(255,255,255,0.05); backdrop-filter: blur(12px); position:relative; z-index:10;
}
.inner-glow { position:absolute; width:50%; height:50%; background:radial-gradient(circle, rgba(126,81,255,0.2) 0%, rgba(0,227,253,0.15) 70%); filter:blur(100px); }
@keyframes float { 0%,100%{transform:translateY(0);}50%{transform:translateY(-15px);} }
.animate-float { animation:float 6s ease-in-out infinite; }

.loading-ring {
  width: 40px; height: 40px; border-radius: 50%;
  border: 2px solid rgba(126,81,255,0.2);
  border-top-color: rgba(126,81,255,0.8);
  animation: spin 0.9s linear infinite;
  position: relative; z-index: 2;
}
@keyframes spin { to { transform: rotate(360deg); } }

select,input { outline:none; border:1px solid rgba(255,255,255,0.2); }
select:focus,input:focus { border-color:#7e51ff; box-shadow:0 0 0 2px rgba(126,81,255,0.3); }
</style>