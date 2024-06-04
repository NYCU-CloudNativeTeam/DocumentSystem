import './assets/main.scss'
import '@mdi/font/css/materialdesignicons.css'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import '@vueup/vue-quill/dist/vue-quill.bubble.css'
import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'


// Vuetify
import 'vuetify/styles'

import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify.ts'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(vuetify)

app.mount('#app')
