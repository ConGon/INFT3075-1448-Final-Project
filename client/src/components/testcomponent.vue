// src/components/AgentTester.vue
<template>
  <div>
    <textarea v-model="task" placeholder="Enter task"></textarea>
    <input v-model="personality" placeholder="Personality"/>
    <input v-model="instructions" placeholder="Instructions"/>
    <button @click="runAgent">Run Agent</button>
    <pre>{{ result }}</pre>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const task = ref('')
const personality = ref('')
const instructions = ref('')
const result = ref('')

const runAgent = async () => {
  try {
    const res = await axios.post('http://localhost:8000/run-agent', {
      task: task.value,
      personality: personality.value,
      instructions: instructions.value
    })
    result.value = res.data.result
  } catch (e) {
    result.value = 'Error: ' + e.message
  }
}
</script>