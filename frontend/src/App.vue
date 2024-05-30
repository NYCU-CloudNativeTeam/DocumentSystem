<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useLinksStore } from '@/stores/links'
import { useUserStore } from '@/stores/user'
import { useTheme } from 'vuetify';

const linksStore = useLinksStore()
const userStore = useUserStore()

const theme = useTheme();

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? 'lightTheme' : 'darkTheme';
}
</script>

<template>
  <v-app>
    <v-navigation-drawer expand-on-hover rail permanent>
      <template v-slot:prepend>
        <v-list>
          <v-list-item prepend-icon="mdi-book" @click="this.$router.push('/')">
            <v-list-item-title class="text-h4 font-weight-bold">DocCenter</v-list-item-title>
          </v-list-item>
        </v-list>
      </template>
      <v-divider thickness="2" color="primary"></v-divider>
      <v-list dense>
        <v-list-item
          v-for="item in linksStore.links"
          :title="item.title"
          :key="item.title"
          :to="item.url"
          :prepend-icon="item.icon"
        >
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <v-divider thickness="2" color="primary"></v-divider>
        <v-list>
          <v-list-item
            :prepend-avatar="userStore.user.avatar"
            :subtitle="userStore.user.email"
            :title="userStore.user.name"
          >
          </v-list-item>
          <v-list-item prepend-icon="mdi-theme-light-dark" @click="toggleTheme" title="SWAP THEME"></v-list-item>
          <v-list-item prepend-icon="mdi-logout" @click="console.log('logout')" title="LOGOUT">
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>
    <RouterView />
  </v-app>
</template>
