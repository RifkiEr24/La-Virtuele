<template>
<div >
 <Navbar/>

   <!-- <Menu>
    <MenuButton> More </MenuButton>
      <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-out"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >

    <MenuItems class="flex flex-col">
      <MenuItem v-slot="{ active }">
        <a :class="{ 'bg-blue-500': active }" href="/account-settings"> Account settings </a>
      </MenuItem>
      <MenuItem v-slot="{ active }">
        <a :class="{ 'bg-blue-500': active }" href="/account-settings"> Documentation </a>
      </MenuItem>
      <MenuItem v-slot="{ active }" disabled>
        <span :class="{ 'bg-blue-500': active }"> Invite a friend (coming soon!) </span>
      </MenuItem>
    </MenuItems>
        </transition>

  </Menu> -->
<router-view v-slot="{ Component }">
  <transition name="fade" mode="out-in">
    <component :is="Component" />
  </transition>
</router-view>
  </div>
</template>
<script>
import  Navbar  from '@/components/Navbar.vue'
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'

export default {
  components: {
    Navbar,
     Menu,
    MenuButton,
    MenuItems,
    MenuItem,
    
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;

}


#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}


.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
