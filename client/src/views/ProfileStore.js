import { reactive } from 'vue'
export const store = reactive({
  profiles: [],
  agents: []
})
export function setAgents(arr) { store.agents = arr }
export function setProfiles(arr) { store.profiles = arr }
export function addProfile(profile) { store.profiles.push(profile) }