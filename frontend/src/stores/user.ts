import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', () => {
  const user = ref({
    name: 'name',
    username: 'abc@test.com',
    avatar: 'https://randomuser.me/api/portraits/women/85.jpg',
    loggedIn: false,
  })

  async function fetchUser() {
    let loggedIn = false;
    try {
      await axios.post('/api/v1/sign-in').then((response) => {
        console.log(response.data);
        user.value.name = response.data.name;
        user.value.username = response.data.username;
        user.value.avatar = response.data.avatar;
        user.value.loggedIn = true;
        loggedIn = true;
      });
    } catch (error) {}
    return loggedIn;
  }

  return { user, fetchUser }
})
