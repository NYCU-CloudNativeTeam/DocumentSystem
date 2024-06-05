<template>
  <v-main>
    <div>
      <v-data-table
        :headers="headers"
        :items="audits"
        class="elevation-1"
        :loading="isLoading"
      >
      <template #item.link="{ item }">
        <v-btn :to="'/documents/' + item.documentUid" color="secondary">VIEW</v-btn>
      </template>
      <template #item.status="{ item }">
        <v-chip
          :color="item.status == 1 ? 'success' : item.status == 3 ? 'warning' : item.status == 2 ? 'error' : 'grey'"
          dark
        >
          {{ item.status == 1 ? 'Approved' : item.status == 3 ? 'Pending' : item.status == 2 ? 'Rejected' : 'Not Sent' }}
          <v-icon class="ml-2" v-if="item.status == 1">mdi-check-decagram</v-icon>
          <v-icon class="ml-2" v-if="item.status == 2">mdi-cancel</v-icon>
          <v-icon class="ml-2" v-if="item.status == 3">mdi-account-clock</v-icon>
          <v-icon class="ml-2" v-if="item.status == 4">mdi-file</v-icon>
        </v-chip>
      </template>
      </v-data-table>
    </div>
  </v-main>
</template>

<script lang="ts">
import axios from 'axios';

export default {
  data () {
    return {
      headers: [
        { title: 'Name', key: 'name' },
        { title: 'Auditor', key: 'auditor' },
        { title: 'Submission Date', key: 'auditCreatedTime' },
        { title: 'Audit Date', key: 'auditedTime' },
        { title: 'View', key: 'link' },
        { title: 'Status', key: 'status' },
      ],
      audits: [
        // { name: 'Document1', auditor: "Sherry Lee", auditedTime: '0000-00-00', auditCreatedTime: '0000-00-00', link: '/documents/123',  status: 1},
      ],
      isLoading: true,
    }
  },
  mounted() {
    axios.get('/api/v1/audits')
      .then(response => {
        this.audits = response.data.documents;
        this.isLoading = false;
      })
  },
}
</script>

<style>
.v-data-table-header__content {
  font-weight: bold;
}
/* @media (min- th: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
} */
</style>
