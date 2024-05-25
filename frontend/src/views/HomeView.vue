<script setup lang="ts"></script>

<template>
  <v-main>
    <v-app-bar height="75">
      <v-btn class="ml-4">NEW DOCUMENT</v-btn>
      <!--
      <v-spacer></v-spacer>
      <v-select
        :items="sortOptions"
        label="Sort by"
        v-model="sort"
        filled
        class="ma-4"
        style="width: 8rem"
      >
      </v-select>
      -->
    </v-app-bar>
    <v-row class="d-flex justify-center">
      <v-card
        class="ma-3 pa-2 d-flex flex-column"
        v-for="document in documents"
        :key="document.uid"
        width="250"
        min-height="380"
        @click="console.log('hi')"
      >
        <v-card-title>
          <p class="text-h5 text--primary text-truncate">{{ document.name }}</p>
        </v-card-title>
        <v-card-text> </v-card-text>
        <v-card-actions>
          <v-btn color="secondary" v-if="document.status == 3">REMIND AGAIN</v-btn>
          <v-spacer></v-spacer>
          <v-icon v-if="document.status == 1">mdi-pencil-outline</v-icon>
          <v-icon v-if="document.status == 2">mdi-eye-outline</v-icon>
          <v-icon v-if="document.status == 3">mdi-account-arrow-right-outline</v-icon>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-main>
</template>

<script lang="ts">
export default {
  data() {
    return {
      sort: null,
      sortOptions: ['Newest', 'Oldest', 'Popular'],
      documents: [
        {
          uid: '1',
          name: 'Document 1',
          status: 1,
          reveal: false
        },
        {
          uid: '2',
          name: 'Document 2222222',
          status: 2,
          reveal: false
        },
        {
          uid: '3',
          name: 'Document 333333333333',
          status: 3,
          reveal: false
        },
        {
          uid: '4',
          name: 'Document 44',
          status: 2,
          reveal: false
        },
        {
          uid: '5',
          name: 'Document 55',
          status: 2,
          reveal: false
        }
      ]
    }
  }
}
</script>
