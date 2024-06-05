<script setup lang="ts"></script>

<template>
  <v-main>
    <v-app-bar height="75">
      <v-btn class="ml-4" @click="createNewDocument">NEW DOCUMENT</v-btn>
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
        class="ma-3 pa-2 d-flex flex-column document-card"
        v-for="document in documents"
        :key="document.uid"
        width="250"
        min-height="380"
        @click="this.$router.push(`/documents/${document.uid}`)"
      >
        <v-card-title>
          <p class="text-h5 text--primary text-truncate">{{ document.name }}</p>
        </v-card-title>
        <v-card-text>
          <QuillEditor contentType="html" v-model:content="document.body" :readOnly="true" toolbar="#invisible-toolbar" height="200px"></QuillEditor>
          <div id="invisible-toolbar"></div>
        </v-card-text>
        <v-card-actions>
          <v-chip
            :color="document.auditStatusColor"
            dark
          >
            {{ document.auditStatusText }}
            <v-icon class="ml-2" v-if="document.auditStatus == 0">mdi-file</v-icon>
            <v-icon class="ml-2" v-if="document.auditStatus == 1">mdi-check-decagram</v-icon>
            <v-icon class="ml-2" v-if="document.auditStatus == 2">mdi-cancel</v-icon>
            <v-icon class="ml-2" v-if="document.auditStatus == 3">mdi-account-clock</v-icon>
          </v-chip>
          <!-- <v-btn color="secondary" v-if="document.status == 3">REMIND AGAIN</v-btn> -->
          <v-spacer></v-spacer>
          <v-icon v-if="document.status == 1">mdi-eye-outline</v-icon>
          <v-icon v-if="document.status == 2">mdi-pencil-outline</v-icon>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-main>
</template>

<script lang="ts">
import axios from 'axios';
import { QuillEditor } from '@vueup/vue-quill'

export default {
  data() {
    return {
      sort: null,
      sortOptions: ['Newest', 'Oldest', 'Popular'],
      documents: [],
    }
  },
  components: {
    QuillEditor
  },
  mounted() {
    axios.get('/api/v1/documents').then((response) => {
      this.documents = response.data['documents'];
      for (let i = 0; i < this.documents.length; i++) {
        this.documents[i].auditStatusColor = document.auditStatus == 1 ? 'success' : document.auditStatus == 2 ? 'error' ? document.auditStatus == 3 : 'warning' : 'grey';
        this.documents[i].auditStatusText = document.auditStatus == 1 ? 'Approved' : document.auditStatus == 2 ? 'Rejected' : document.auditStatus == 3 ? 'Pending' : 'Not Sent';
      }
      console.log(this.documents);
      // for (let i = 0; i < this.documents.length; i++) {
      //   this.documents[i].reveal = false;
      // }
    });
  },
  methods: {
    createNewDocument() {
      axios.post('/api/v1/documents').then((response) => {
        this.$router.push(`/documents/${response.data['documentUid']}`);
      });
    }
  }
}
</script>
