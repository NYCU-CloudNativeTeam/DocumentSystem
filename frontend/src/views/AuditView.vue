<template>
  <v-main>
    <div>
      <v-data-table
        :headers="headers"
        :items="employees"
        class="elevation-1"
      ></v-data-table>
    </div>
  </v-main>
</template>
  
<script lang="ts">
  export default {
    data () {
      return {
        headers: [
          {
            title: 'Title',
            // align: 'start',
            // sortable: true,
            key: 'title',
          },
          { title: 'Name', key: 'name' },
          { title: 'Submission Date', key: 'submissiondate' },
          { title: 'Audit Date', key: 'auditdate' },
          { title: 'View', key: 'link' },
          { title: 'Status', key: 'status' },
        ],
        employees: [
          { title: 'Document1', name: "Sherry Lee", submissiondate: '0000-00-00', auditdate: '0000-00-00', link: 'google.com',  status: 'Active'},
          { title: 'Document2', name: "Ross Geller", submissiondate: '0000-00-00', auditdate: '0000-00-00' , link: '', status: 'Active'},
          { title: 'Document3', name: "Rachel Green", submissiondate: '0000-00-00',  auditdate: '0000-00-00', link: '',  status: 'Active'},
          { title: 'Document4', name: "Rachel Green", submissiondate: '0000-00-00',  auditdate: '0000-00-00', link: '',  status: 'Active'},
          { title: 'Document5', name: "Joey Tribbiani", submissiondate: '0000-00-00',  auditdate: '0000-00-00' , link: '',  status: 'Active'},
          { title: 'Document6', name: "Phoebe Buffay", submissiondate: '0000-00-00', auditdate: '0000-00-00' , link: '', status: 'Active'},
          { title: 'Document7', name: "Chandler Bing", submissiondate: '0000-00-00', auditdate: '0000-00-00' , link: '', status: 'Active'},
          { title: 'Document8', name: "Ross Geller", submissiondate: '0000-00-00', auditdate: '0000-00-00' , link: '', status: 'Active'},
          { title: 'Document9', name: "Rachel Green", submissiondate: '0000-00-00',  auditdate: '0000-00-00', link: '',  status: 'Active'},
          { title: 'Document10', name: "Monica Geller", submissiondate: '0000-00-00',  auditdate: '0000-00-00' , link: '',  status: 'Active'},
          { title: 'Document11', name: "Joey Tribbiani", submissiondate: '0000-00-00', auditdate: '0000-00-00' , link: '',  status: 'Active'},
          { title: 'Document12', name: "Phoebe Buffay", submissiondate: '0000-00-00',  auditdate: '0000-00-00' , link: '', status: 'Active'}
        ],
      }
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
