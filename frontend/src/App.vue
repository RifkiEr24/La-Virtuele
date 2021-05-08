<template>
  <div>
  <Navbar/>
<vue-page-transition name="fade">
<router-view v-slot="{ Component }">
    <component :is="Component" />
</router-view>
  </vue-page-transition>

  </div>
</template>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
<script>
import Navbar from '@/components/Navbar.vue';

export default {
  components: {
    Navbar,
  },
};
</script>
