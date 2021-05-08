import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import './assets/css/styles.css'
import './assets/css/tailwind.css';
import VuePageTransition from 'vue-page-transition'
 
Vue.use(VuePageTransition)
Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
