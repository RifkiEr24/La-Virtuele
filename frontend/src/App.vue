<template>
  <div>
  <Navbar/>
<vue-page-transition name="fade">
<router-view :class="{ 'pt-16': $route.path != '/' }" v-slot="{ Component }">
    <component :is="Component" />
</router-view>
  </vue-page-transition>

  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
export default {
  components: {
    Navbar,
  },
};
</script>
