import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useLinksStore = defineStore('links', () => {
  const links = ref([
    {
      title: 'Documents',
      url: '/',
      icon: 'mdi-file-document-outline'
    },
    {
      title: 'Audits',
      url: '/about',
      icon: 'mdi-eye-outline'
    }
  ])

  return { links }
})
