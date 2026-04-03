<template>
  <div class="relative h-screen bg-[#0c0e17] text-white overflow-hidden">
    <router-view></router-view>
    <nav class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-8 pb-4 h-20 bg-[#0c0e17]/80 backdrop-blur-xl rounded-t-[2rem]">
      <button
        @click="$router.push('/add')"
        :class="$route.path === '/add' ? 'text-[#00e3fd]' : 'text-[#aaaab7]'"
        class="flex flex-col items-center justify-center p-2 transition-colors"
      >
        <span class="material-symbols-outlined text-3xl">add</span>
        <span class="text-xs">Add</span>
      </button>
      <button
        @click="$router.push('/')"
        :class="$route.path === '/' ? 'text-[#00e3fd]' : 'text-[#aaaab7]'"
        class="flex flex-col items-center justify-center p-2 transition-colors"
      >
        <span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">home</span>
        <span class="text-xs">Main</span>
      </button>
      <button
        @click="$router.push('/edit')"
        :class="$route.path.startsWith('/edit') ? 'text-[#00e3fd]' : 'text-[#aaaab7]'"
        class="flex flex-col items-center justify-center p-2 transition-colors"
      >
        <span class="material-symbols-outlined text-3xl">edit</span>
        <span class="text-xs">Edit</span>
      </button>
    </nav>
  </div>
</template>

<script setup></script>