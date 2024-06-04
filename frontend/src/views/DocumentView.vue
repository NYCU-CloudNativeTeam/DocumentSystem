<script setup lang="ts">
import { ref, watch } from 'vue';
import { useDebounceFn } from '@vueuse/core';

const searchedUsers = ref([]);
const searchLoading = ref(false);
const selectedUser = ref(null);
const isPermissionsEditting = ref(false);
const isPermissionsLoading = ref(false);
const permissions = ref([]);

const props = defineProps({
  uid: String,
});

const searchUsers = useDebounceFn((input) => {
  if (input.length == 0) {
    searchedUsers.value = [];
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
  })}, 500);

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
          v-if="mode === 2"
        ></v-btn>
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn color="secondary" @click="openPermissionsEdittingDialog" v-if="mode === 2">PERMISSION</v-btn>
      <v-btn color="primary" @click="saveDocument" v-if="mode === 2">SAVE</v-btn>
      <v-btn color="primary" v-if="mode === 2">AUDIT</v-btn>
    </v-app-bar>
    <div class="document">
      <QuillEditor
        :options="options"
        contentType="html"
        v-model:content="content"
        @contextmenu="onContextMenu"
        @selectionChange="onSelectionChange"
        @textChange="onTextChange"
        :toolbar="mode === 2 ? 'full' : '#no-toolbar'"
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
            prepent-inner-icon="mdi-magnify"
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
      otherIsEditing: false,
      permissionHeaders: [
        { title: 'Name', key: 'name' },
        { title: 'Username', key: 'username' },
        { title: 'Permission', key: 'permissionType' },
      ],
      mode: 1,
      isDocumentLoaded: false,
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
    axios.get('/api/v1/documents/' + this.uid)
      .then(response => {
        this.name = response.data.name;
        this.content = response.data.body;
        this.otherIsEditing = response.data.otherIsEditing;
        this.mode = response.data.mode;
        this.isDocumentLoaded = true;
      })
      .catch(error => {
        console.log(error);
      });
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
  methods: {
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
      axios.put('/api/v1/documents/' + this.uid, {
        body: this.$refs.quillEditor.getHTML(),
        comments: [],
      }).then(response => {
        console.log(response);
      }).catch(error => {
        console.log(error);
      });
    },
  }
};
</script>
