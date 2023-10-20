/* eslint-disable vue/no-reserved-component-names */
/* eslint-disable vue/multi-word-component-names */
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import '@/assets/main.css'
import 'primevue/resources/themes/lara-light-indigo/theme.css'
import Button from 'primevue/button'
import PrimeVue from 'primevue/config'
import FileUpload from 'primevue/fileupload'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.use(PrimeVue)
app.component('Button', Button)
app.component('FileUpload', FileUpload)

app.mount('#app')
