<template>
  <div class="relative h-screen bg-[#0c0e17] text-white overflow-hidden">
    <!-- Page Content -->
    <router-view></router-view>

    <!-- Bottom Navbar -->
    <nav class="fixed bottom-0 left-0 w-full z-50 flex justify-around items-center px-8 pb-4 h-20 bg-[#0c0e17]/80 backdrop-blur-xl rounded-t-[2rem]">
      <button
        @click="$router.push('/add')"
        :class="{'text-[#00e3fd]': $route.path === '/add', 'text-[#aaaab7]': $route.path !== '/add'}"
        class="flex flex-col items-center justify-center p-2 transition-colors"
      >
        <span class="material-symbols-outlined text-3xl">add</span>
        <span class="text-xs">Add</span>
      </button>

      <button
        @click="$router.push('/')"
        :class="{'text-[#00e3fd]': $route.path === '/', 'text-[#aaaab7]': $route.path !== '/'}"
        class="flex flex-col items-center justify-center p-2 transition-colors"
      >
        <span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">home</span>
        <span class="text-xs">Main</span>
      </button>

      <button
        @click="$router.push('/edit')"
        :class="{'text-[#00e3fd]': $route.path === '/edit', 'text-[#aaaab7]': $route.path !== '/edit'}"
        class="flex flex-col items-center justify-center p-2 transition-colors"
      >
        <span class="material-symbols-outlined text-3xl">edit</span>
        <span class="text-xs">Edit</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
// App.vue is now just the shell; router handles views
</script>

<style scoped>
/* Optional: any global navbar tweaks */
</style>