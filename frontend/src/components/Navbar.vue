<template>
    <nav  v-scroll="updateScroll" :class="{'md:bg-secondary': scrollPosition > 20}" class="flex-row block md:flex fixed  z-50 transition duration-500 mx-auto md:justify-between  w-full  h-12 bg-secondary md:bg-transparent py-0 uppercase ">
      <modal name="my-first-modal">
        This is my first modal
    </modal>
      <div class="flex flex-row w-full md:w-5/12 justify-between px-4 " :class="{ 'text-white': $route.path === '/' ||  scrollPosition > 20  }">
           <a href="#" class="p-2  text-3xl header">La.virtuele</a>

           <svg class="text-white w-8 text-sm md:hidden accesibillity-size"  id="hamburgerbtn" @click="active" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </div>

        <ul :class="{'md:text-white': scrollPosition > 20}" class="transform -translate-x-full md:translate-x-0 -translate-y-2 md:translate-y-0 mx-auto md:flex text-center bg-secondary md:bg-transparent text-white  md:text-black w-full md:w-5/12 md:flex-row transition transition-75 duration-300" ref="mobileMenu" id="mobileMenu">
           <li class="md:px-6 md:py-2.5 transition duration-500 ease-in-out p-0     md:mt-0">   <router-link to="/">  Home </router-link> </li>
          <li class="md:px-6 md:py-2.5 transition duration-500 p-0   mt-2 md:mt-0"> <router-link to="about"> Shop</router-link></li>
            <li class="md:px-6 transition duration-500 md:py-2.5 p-0   mt-2 md:mt-0"><a>Article</a></li>
        <li class="flex md:hidden">
          <div class="relative flex mx-auto flex-wrap my-2 items-stretch mb-3">
            <span
              class="z-10 h-full  leading-snug font-normal absolute text-center text-gray-400 absolute bg-transparent rounded text-base items-center justify-center w-8 p-2 py-4">
              <svg class="text-primary stroke-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input type="text" placeholder="search"
              class="px-5 py-0 accesibillity-size w-48 placeholder-gray-400  text-black relative bg-white bg-white rounded  shadow outline-none focus:outline-none focus:shadow-outline pl-10" />
          </div>
        </li>
        </ul>
        <div class="hidden w-12/12 md:w-2/12 md:flex  justify-end items-center " ref="search">
          <div class="mx-4">
            <span :class="{'text-white': scrollPosition > 20 , 'text-gray-400' : scrollPosition < 20}" >Login</span>
          </div>
          <div :class="{'text-white': scrollPosition > 20}"  class="text-primary   mx-5 text-2xl" >
          <span class="iconify" data-icon="bi:cart" data-inline="false"></span>

          </div>

        </div>
    </nav>
</template>
<script>
import Login from './Login.vue'

export default {
  name: 'Navbar',
  data(){
    return{
      scrollPosition: null,
      
    }
  },
  methods: {
    active() {
      this.$refs.mobileMenu.classList.toggle('-translate-x-full');
    },
     updateScroll() {
       this.scrollPosition = window.scrollY
    }
    
  },
  mounted(){
            this.$modal.show(
  Login,

)

        window.addEventListener('scroll', this.updateScroll);

  }
};
</script>
<style>
 .active{
        display: block;
    }

</style>
