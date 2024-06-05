<script setup lang="ts">
import { ref, watch } from 'vue';
import { useDebounceFn } from '@vueuse/core';
import { useRouter } from 'vue-router'

const searchedUsers = ref([]);
const searchLoading = ref(false);
const selectedUser = ref(null);
const selectedAuditor = ref(null);
const isPermissionsEditting = ref(false);
const isPermissionsLoading = ref(false);
const isAuditing = ref(false);
const permissions = ref([]);
const router = useRouter();
const saveDocumentButton = ref(null);
const quillEditor = ref(null);
const isRejectionEditting = ref(false);
const rejectionInEditting = ref('');

const props = defineProps({
  uid: String,
});

const searchUsers = useDebounceFn((input) => {
  if (input.length == 0) {
    return;
  }
  searchLoading.value = true;
  axios.get('/api/v1/users', {
    params: {
      'search-text': input,
      'document-uid': props.uid,
    }
  }).then(response => {
    searchedUsers.value = response.data;
    searchLoading.value = false;
  }).catch(error => {
    console.log(error);
  })}, 200);

watch(selectedUser, (newValue) => {
  if (!newValue) {
    return;
  }
  axios.put('/api/v1/documents/' + props.uid + '/permissions', {
    username: newValue,
    permissionType: 1,
  }).then(response => {
    console.log(response);
    getPermissions();
  }).catch(error => {
    console.log(error);
  });
  selectedUser.value = null;
});

function closeRejectionEdittingDialogWithSaving() {
  axios.post('/api/v1/documents/' + props.uid + '/audit-result', {
    auditStatus: 2,
    rejectedReason: rejectionInEditting.value,
  }).then(response => {
    console.log(response);
    router.go();
  }).catch(error => {
    console.log(error);
  });
  isRejectionEditting.value = false;
  rejectionInEditting.value = '';
}

function closeRejectionEdittingDialogWithoutSaving() {
  isRejectionEditting.value = false;
  rejectionInEditting.value = '';
}

function getPermissions() {
  isPermissionsLoading.value = true;
  axios.get('/api/v1/documents/' + props.uid + '/permissions')
    .then(response => {
      isPermissionsLoading.value = false;
      if (!response.data.permissions) {
        permissions.value = []
      } else {
        permissions.value = response.data.permissions;
      }
    })
    .catch(error => {
      isPermissionsLoading.value = false;
    });
}

function openPermissionsEdittingDialog() {
  isPermissionsEditting.value = true;
  getPermissions();
}

function closePermissionsEdittingDialog() {
  isPermissionsEditting.value = false;
}

function openAuditingDialog() {
  isAuditing.value = true;
}

function closeAuditingDialog() {
  isAuditing.value = false;
}

function approveAudit() {
  axios.post('/api/v1/documents/' + props.uid + '/audit-result', {
    auditStatus: 1,
    rejectedReason: '',
  }).then(response => {
    console.log(response);
    router.go();
  }).catch(error => {
    console.log(error);
  });
}

function rejectAudit() {
  isRejectionEditting.value = true;
}

function sendAuditRequest() {
  axios.put('/api/v1/documents/' + props.uid, {
    body: quillEditor.value.getHTML(),
    comments: [],
  }).then(response => {
    console.log(response);
    axios.post('/api/v1/audits', {
      documentUid: props.uid,
      auditorUsername: selectedAuditor.value,
    }).then(response => {
      console.log(response);
      router.go();
    }).catch(error => {
      console.log(error);
    });
    isAuditing.value = false;
    selectedAuditor.value = null;
  }).catch(error => {
    console.log(error);
  });
}

function changePermission(item, event) {
  axios.put('/api/v1/documents/' + props.uid + '/permissions', {
    username: item.username,
    permissionType: event,
  }).then(response => {
    console.log(response);
  }).catch(error => {
    console.log(error);
  });
}
</script>
<template>
  <v-main>
    <v-app-bar height="75">
      <v-btn icon @click="goBack">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-app-bar-title>
        {{ name }}
        <v-btn
          class="ml-2"
          density="compact"
          icon="mdi-pencil"
          @click="openNameEdittingDialog"
          v-if="mode === 2 && auditStatus !== 3"
          ></v-btn>
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-sheet class="border pa-3 mr-3" rounded>
        <span>Audit Status:</span>
        <v-chip
          class="ml-2"
          :color="auditStatusChipColor"
        >
          {{ auditStatusChipText }}
          <v-icon class="ml-2" v-if="auditStatus == 1">mdi-check-decagram</v-icon>
          <v-icon class="ml-2" v-if="auditStatus == 2">mdi-cancel</v-icon>
          <v-icon class="ml-2" v-if="auditStatus == 3">mdi-account-clock</v-icon>
          <v-icon class="ml-2" v-if="auditStatus == 4">mdi-file</v-icon>
        </v-chip>
        <v-btn class="ml-2" color="primary" @click="openAuditingDialog" append-icon="mdi-send" v-if="canEdit && auditStatus === 4">AUDIT</v-btn>
        <v-btn class="ml-2" color="primary" @click="approveAudit" v-if="canAudit" append-icon="mdi-hand-okay">APPROVE</v-btn>
        <v-btn class="ml-2" color="error" @click="rejectAudit" v-if="canAudit" append-icon="mdi-close-thick">REJECT</v-btn>
      </v-sheet>
      <v-btn color="secondary" @click="openPermissionsEdittingDialog" v-if="mode === 2" append-icon="mdi-account">PERMISSION</v-btn>
      <v-btn ref="saveDocumentButton" color="primary" @click="saveDocument" v-if="canEdit" append-icon="mdi-content-save">SAVE</v-btn>
    </v-app-bar>
    <div class="document">
      <QuillEditor
        :options="options"
        contentType="html"
        v-model:content="content"
        @contextmenu="onContextMenu"
        @selectionChange="onSelectionChange"
        @textChange="onTextChange"
        :toolbar="canEdit ? 'full' : '#no-toolbar'"
        ref="quillEditor"
        :readOnly="mode !== 2"
        v-if="isDocumentLoaded"
      >
        <template #toolbar>
          <div id="no-toolbar">
          </div>
          <!--
          <div id="custom-toolbar">
            <select class="ql-background"></select>
            <button class="ql-link"></button>
            <button class="ql-image"></button>
            <v-btn class="elevation-0" style="width: fit-content" @click="addComment">COMMENT</v-btn>
          </div>
          -->
        </template>
      </QuillEditor>
    </div>
    <v-dialog v-model="isNameEditting" width="30%">
      <v-card>
        <v-card-title class="text-h6">
          Name
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="nameInEditting" outlined></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="closeNameEdittingDialogWithSaving">OK</v-btn>
          <v-btn text color="secondary" @click="closeNameEdittingDialogWithoutSaving">CANCEL</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="isRejectionEditting" width="30%">
      <v-card>
        <v-card-title class="text-h6">
          Rejected Reason
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="rejectionInEditting" outlined></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="closeRejectionEdittingDialogWithSaving">OK</v-btn>
          <v-btn text color="secondary" @click="closeRejectionEdittingDialogWithoutSaving">CANCEL</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="isPermissionsEditting" width="50%">
      <v-card>
        <v-card-title class="text-h6">
          Permissions
        </v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="selectedUser"
            :items="searchedUsers"
            :loading="searchLoading"
            prepend-inner-icon="mdi-magnify"
            menu-icon=""
            density="comfortable"
            placeholder="Search user"
            item-props
            item-title="username"
            item-value="username"
            @update:search="searchUsers"
          >
          <template v-slot:item="{ props, item }">
            <v-list-item
              v-bind="props"
              :prepend-avatar="item.raw.profilePictureUrl"
              append-icon="mdi-account-plus"
              :title="item.raw.name"
              :subtitle="item.raw.username"
            ></v-list-item>
          </template>
          </v-autocomplete>
          <v-data-table
            :headers="permissionHeaders"
            :items="permissions"
            :loading="isPermissionsLoading"
          >
          <template #item.permissionType="{ item }">
            <v-select
              :items="[
                { text: 'Read', value: 1 },
                { text: 'Write', value: 2 }
              ]"
              item-title="text"
              item-value="value"
              v-model="item.permissionType"
              density="compact"
              @update:modelValue="changePermission(item, $event)"
            ></v-select>
          </template>
          </v-data-table>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="primary" @click="closePermissionsEdittingDialog">CLOSE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="isAuditing" width="50%">
      <v-card>
        <v-card-title class="text-h6">
          Audit
        </v-card-title>
        <v-card-text>
          <v-autocomplete
            v-model="selectedAuditor"
            :items="searchedUsers"
            :loading="searchLoading"
            prepend-inner-icon="mdi-magnify"
            menu-icon=""
            density="comfortable"
            placeholder="Search user"
            item-props
            item-title="username"
            item-value="username"
            @update:search="searchUsers"
            chips
          >
          <template v-slot:chip="{ props, item }">
            <v-chip
              v-bind="props"
              color="primary"
              :text="item.raw.username"
              :prepend-avatar="item.raw.profilePictureUrl"
            ></v-chip>
          </template>
          <template v-slot:item="{ props, item }">
            <v-list-item
              v-bind="props"
              :prepend-avatar="item.raw.profilePictureUrl"
              :title="item.raw.name"
              :subtitle="item.raw.username"
            ></v-list-item>
          </template>
          </v-autocomplete>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text color="priamry" @click="sendAuditRequest">SEND</v-btn>
          <v-btn text color="secondary" @click="closeAuditingDialog">CLOSE</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-main>
</template>

<script lang="ts">
import { QuillEditor } from '@vueup/vue-quill'
import ContextMenu from '@imengyu/vue3-context-menu'
import axios from 'axios'

export default {
  data() {
    return {
      name: '',
      isNameEditting: false,
      nameInEditting: '',
      content: '',
      options: {
        theme: 'snow',
        modules: {
          // toolbar: '#custom-toolbar',
        },
      },
      otherIsEditting: false,
      permissionHeaders: [
        { title: 'Name', key: 'name' },
        { title: 'Username', key: 'username' },
        { title: 'Permission', key: 'permissionType' },
      ],
      mode: 1,
      isDocumentLoaded: false,
      auditStatus: 1,
      auditStatusChipText: '',
      auditStatusChipColor: '',
      canEdit: false,
      canAudit: false,
      // selectedRange: null,
      commentId: 0,
    }
  },
  props: ['uid'],
  components: {
    QuillEditor
  },
  mounted() {
    window.addEventListener('beforeunload', (event) => {
      return true;
    });
    window.addEventListener('unload', (event) => {
      axios.delete('/api/v1/documents/' + this.uid + '/lock-session', {
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      });
    });
    this.loadDocument();
  },
  unmounted() {
    window.removeEventListener('beforeunload', (event) => {
      return true;
    });
    window.removeEventListener('unload', (event) => {
      axios.delete('/api/v1/documents/' + this.uid + '/lock-session', {
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      });
    });
    axios.delete('/api/v1/documents/' + this.uid + '/lock-session', {
    }).then(response => {
      console.log(response);
    }).catch(error => {
      console.log(error);
    });
  },
  watch: {
    mode: {
      handler: function(newValue) {
        this.canEdit = this.auditStatus !== 3 && this.mode === 2;
        this.canAudit = this.auditStatus === 3 && this.mode === 3;
      },
      immediate: true,
    },
    auditStatus: {
      handler: function(newValue) {
        this.auditStatusChipText = newValue === 4 ? 'Not Sent' : newValue === 1 ? 'Approved' : newValue === 2 ? 'Rejected' : 'Pending';
        this.auditStatusChipColor = newValue === 4 ? 'grey' : newValue === 1 ? 'success' : newValue === 2 ? 'error' : 'warning';
        this.canEdit = this.auditStatus !== 3 && this.mode === 2;
        this.canAudit = this.auditStatus === 3 && this.mode === 3;
      },
      immediate: true,
    },
  },
  methods: {
    loadDocument() {
      axios.get('/api/v1/documents/' + this.uid)
        .then(response => {
          this.name = response.data.name;
          this.content = response.data.body;
          this.otherIsEditting = response.data.otherIsEditting;
          this.mode = response.data.mode;
          this.isDocumentLoaded = true;
          this.auditStatus = response.data.auditStatus;
        })
        .catch(error => {
          console.log(error);
        });
    },
    goBack() {
      this.$router.go(-1)
    },
    openNameEdittingDialog() {
      this.isNameEditting = true;
      this.nameInEditting = this.name;
    },
    closeNameEdittingDialogWithSaving() {
      axios.put('/api/v1/documents/' + this.uid + '/name', {
        name: this.nameInEditting,
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      });
      this.name = this.nameInEditting;
      this.isNameEditting = false;
    },
    closeNameEdittingDialogWithoutSaving() {
      this.isNameEditting = false;
    },
    onSelectionChange({ range, oldRange, source }) {
      this.selectedRange = range;
      // let character = this.$refs.quillEditor.getContents(this.selectedRange.index, this.selectedRange.length);
      // console.log(this.selectedRange.index, this.selectedRange.length);
      // console.log(character);
    },
    onTextChange(data) {
      let text = this.$refs.quillEditor.getText();
      if (text.length == 1 && text[0] == '\n') {
        this.$refs.quillEditor.setHTML('<p><br></p>');
      }
    },
    onContextMenu(e : MouseEvent) {
      e.preventDefault();
      //show your menu
      ContextMenu.showContextMenu({
        x: e.x,
        y: e.y,
        items: [
          {
            label: 'Copy',
            onClick: () => {
              navigator.clipboard.writeText(window.getSelection().toString());
            }
          },
          {
            label: 'Paste',
            onClick: () => {
              const newText = navigator.clipboard.readText();
            }
          },
          /*
          {
            label: "A submenu",
            children: [
              { label: "Item1" },
              { label: "Item2" },
              { label: "Item3" },
            ]
          },
          */
        ]
      });
    },
    // addComment() {
    //   console.log(this.selectedRange);
    //   let content = this.$refs.quillEditor.getHTML();
    //   // Check if there is any text selected
    //   if (this.selectedRange.length == 0) {
    //     alert('Please select some text to comment on.');
    //     return;
    //   }
    //   // Check if the selected texts don't contain a br
    //   if (this.$refs.quillEditor.getText(this.selectedRange.index, this.selectedRange.length).includes('\n')) {
    //     alert('Please select a continuous text to comment on.');
    //     return;
    //   }
    //   // Check if there's already a comment on the selected text
    //   let counter = 0;
    //   let skip = false;
    //   let htmlEntityCounter = 0;
    //   let commentStart = this.selectedRange.index;
    //   let commentEnd = this.selectedRange.index + this.selectedRange.length;
    //   let insideOldComment = false;
    //   let insideNewComment = false;
    //   for (let i = 0; i < content.length; i++) {
    //     if (counter === commentStart) {
    //       insideNewComment = true;
    //     } else if (counter === commentEnd) {
    //       insideNewComment = false;
    //     }
    //     if (content[i] === '<') {
    //       skip = true;
    //       console.log('hi');
    //       console.log(content.substring(i, i + 4));
    //       console.log(content.substring(i, i + 27));
    //       if (content.substring(i, i + 4) === '<img') {
    //         counter++;
    //       }
    //       if (content.substring(i, i + 27) === '<span class="quill-comment"') {
    //         insideOldComment = true;
    //       } else if (content.substring(i, i + 7) === '</span>') {
    //         insideOldComment = false;
    //       }
    //       continue;
    //     } else if (content[i] === '>') {
    //       skip = false;
    //       continue;
    //     }
    //     if (!skip) {
    //       if (content[i] === '&') {
    //         htmlEntityCounter++;
    //       } else if (content[i] === ';') {
    //         counter -= htmlEntityCounter;
    //         htmlEntityCounter = 0;
    //       } else if (htmlEntityCounter != 0) {
    //         htmlEntityCounter++;
    //       }
    //       counter++;
    //       console.log(content[i], counter);
    //     }
    //     if (insideOldComment && insideNewComment) {
    //       alert('There is already a comment on the selected text.');
    //       return;
    //     }
    //   }
    //   // Find the correct position to insert the comment
    //   const commentHeadHtml = '<span class="quill-comment" id="#comment-' + this.commentId + '" style="background: red;">';
    //   const commentTailHtml = '</span>';
    //   this.commentId++;
    //   counter = 0;
    //   skip = false;
    //   htmlEntityCounter = 0;
    //   commentStart = this.selectedRange.index;
    //   commentEnd = this.selectedRange.index + this.selectedRange.length;
    //   let newContent = content;
    //   for (let i = 0; i < content.length; i++) {
    //     if (counter == commentStart) {
    //       console.log('asdfasdgasdfagsafs');
    //       newContent = content.substring(0, i) + commentHeadHtml + content.substring(i);
    //     } else if (counter == commentEnd) {
    //       newContent = newContent.substring(0, i + commentHeadHtml.length) + commentTailHtml + newContent.substring(i + commentHeadHtml.length);
    //       break;
    //     }
    //     if (content[i] === '<') {
    //       skip = true;
    //       if (content.substring(i, i + 5) === '<img') {
    //         counter++;
    //       }
    //       continue;
    //     } else if (content[i] === '>') {
    //       skip = false;
    //       continue;
    //     }
    //     if (!skip) {
    //       if (content[i] === '&') {
    //         htmlEntityCounter++;
    //       } else if (content[i] === ';') {
    //         counter -= htmlEntityCounter;
    //         htmlEntityCounter = 0;
    //       } else if (htmlEntityCounter != 0) {
    //         htmlEntityCounter++;
    //       }
    //       counter++;
    //     }
    //   }
    //   console.log(this.selectedRange);
    //   console.log(content);
    //   console.log(newContent);
    //   this.$refs.quillEditor.setHTML(newContent);
    //   console.log(this.$refs.quillEditor.getHTML());
    // },
    saveDocument() {
      if (this.auditStatus === 1 || this.auditStatus === 2) {
        if (confirm('Do you want to save the document? The audit will be rolled back to the "Not Sent" status.')) {
          axios.put('/api/v1/documents/' + this.uid, {
            body: this.$refs.quillEditor.getHTML(),
            comments: [],
          }).then(response => {
            console.log(response);
            this.$router.go();
          }).catch(error => {
            console.log(error);
          });
        }
      } else {
        axios.put('/api/v1/documents/' + this.uid, {
          body: this.$refs.quillEditor.getHTML(),
          comments: [],
        }).then(response => {
          console.log(response);
        }).catch(error => {
          console.log(error);
        });
      }
    },
  }
};
</script>
