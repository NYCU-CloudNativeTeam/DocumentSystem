import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref({
    name: 'username',
    email: 'abc@gmail.com',
    avatar: 'https://randomuser.me/api/portraits/women/85.jpg'
  })

  return { user }
})
