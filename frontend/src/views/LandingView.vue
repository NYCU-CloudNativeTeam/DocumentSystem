<script setup lang="ts">
import { useUserStore } from '@/stores/user'
import { useRouter, useRoute } from 'vue-router'

const userStore = useUserStore();
const router = useRouter();

if (userStore.user.loggedIn) {
  router.push('/');
}
</script>
<template>
  <v-container>
    <v-row>
      <v-col lg="6">
        <h2 class="intro-text">Welcome to the Document Center</h2>
        <!-- <p class="description">Hi</p> -->
        <v-btn color = "indigo" class="white--text" rounded height="45" href="/api/v1/sign-in">
          Login Using <span class="font-weight-black pl-1">Google</span>
          <!-- <v-icon right>mdi-login</v-icon> -->
        </v-btn>
      </v-col>
      <v-col lg="6">
        <v-img src="/discussion.png"></v-img>
      </v-col>
      </v-row>
  </v-container>
</template>

<script lang="ts">
import axios from 'axios';

export default {
  name: "LandingView",
}
</script>

<style scoped>
 h2.intro-text {
   font-size: 4rem;
   font-weight: 700;
   margin-bottom: 1rem;

 }
 .v-col {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.fixed-button {
  width: 170px;
  height: 50px;
}
</style>
