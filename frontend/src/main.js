import Vue from 'vue';
import App from './App.vue';
import './registerServiceWorker';
import router from './router';
import './assets/css/styles.css'
import './assets/css/tailwind.css';
import VuePageTransition from 'vue-page-transition'
import Transitions from 'vue2-transitions'
import VueAxios from 'vue-axios';

import axios from 'axios'

  import 'vue-slick-carousel/dist/vue-slick-carousel.css'
  // optional style for arrows & dots
  import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'

  Vue.directive('scroll', {
    inserted: function (el, binding) {
      let f = function (evt) {
        if (binding.value(evt, el)) {
          window.removeEventListener('scroll', f)
        }
      }
      window.addEventListener('scroll', f)
    }
  })
  
Vue.use(Transitions)
Vue.use(VuePageTransition)
Vue.config.productionTip = false;
Vue.use(VueAxios, axios);
new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
