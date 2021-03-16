import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/css/tailwind.css'
import './assets/css/styles.css'
import 'alpinejs'

createApp(App).use(router).mount('#app')
