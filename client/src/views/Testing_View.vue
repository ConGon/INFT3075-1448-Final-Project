<template>
  <div class="relative h-screen flex items-center justify-center bg-[#0c0e17]">
    <!-- Settings Drawer -->
    <div class="settings-drawer fixed top-0 left-0 w-full z-[60] bg-[#11131d] flex flex-col" id="settings-drawer">
      <div class="flex-1 p-8 flex flex-col justify-center">
        <div class="p-6 rounded-xl border border-outline-variant/30 bg-[#1c1f2b] flex items-center justify-center">
          <span class="font-headline font-bold tracking-widest text-on-surface text-lg">AGENT</span>
        </div>
        <div class="p-6 rounded-xl border border-outline-variant/30 bg-[#1c1f2b] flex items-center justify-center">
          <span class="font-headline font-bold tracking-widest text-on-surface text-lg">MODE</span>
        </div>
        <div class="p-6 rounded-xl border border-outline-variant/30 bg-[#1c1f2b] flex items-center justify-center">
          <span class="font-headline font-bold tracking-widest text-on-surface text-lg">PROMPT</span>
        </div>
      </div>
      <div class="settings-handle" @click="toggleSettings">
        <span class="material-symbols-outlined text-outline transition-transform duration-500" id="handle-icon">
          expand_more
        </span>
      </div>
    </div>

    <!-- Crystal Ball -->
    <div class="crystal-ball animate-float relative z-10">
      <div class="inner-glow"></div>
      <div
        ref="aiTextRef"
        class="text-center text-purple-400 font-bold select-none"
        style="line-height: 1.05; padding: 0 12px;"
      >
        <template v-for="(line, index) in formattedLines" :key="index">
          <div>{{ line }}</div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue'

const aiText = ref('Your AI output will appear here!')
const aiTextRef = ref(null)

function fitFont() {
  nextTick(() => {
    if (!aiTextRef.value) return
    const ballSize = 280
    let currentFontSize = 48
    aiTextRef.value.style.fontSize = currentFontSize + 'px'
    while (
      (aiTextRef.value.scrollWidth > ballSize * 0.85 ||
        aiTextRef.value.scrollHeight > ballSize * 0.85) &&
      currentFontSize > 8
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
.settings-drawer {
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateY(calc(-100% + 48px));
}
.settings-drawer.is-open {
  transform: translateY(0);
}
.settings-handle {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}
.crystal-ball {
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.15), rgba(255,255,255,0) 70%),
              radial-gradient(circle at 50% 50%, rgba(126,81,255,0.1), rgba(0,227,253,0.05));
  box-shadow: 
    inset 0 0 50px rgba(126,81,255,0.2),
    inset 0 0 20px rgba(0,227,253,0.2),
    0 0 60px rgba(126,81,255,0.1),
    0 0 100px rgba(0,227,253,0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  position: relative;
  z-index: 10;
}
.inner-glow {
  position: absolute;
  width: 80%;
  height: 80%;
  background: radial-gradient(circle, rgba(126,81,255,0.2) 0%, rgba(0,227,253,0.15) 70%);
  filter: blur(20px);
}
@keyframes float { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-15px); } }
.animate-float { animation: float 6s ease-in-out infinite; }
</style>