<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
</script>

<template>
  <main>
    {{ userStore.user }}
  </main>
</template>
