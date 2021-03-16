<template>
    <nav class="flex-row transition-transform mx-auto md:justify-between shadow-xl md:flex text-white h-12 bg-secondary p-8 py-0 uppercase">
        <div class="flex flex-row w-12/12 md:w-4-12 justify-between">
           <a href="#" class="p-2  text-3xl header">La.virtuele</a>

           <svg class="text-white w-8 text-sm md:hidden"  id="hamburgerbtn" @click="active" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </div>
       
        <ul class="hidden mx-auto md:flex  w-12/12 md:w-4-12 md:flex-row transition" ref="mobileMenu" id="mobileMenu">
            <li class="md:px-6 md:py-2.5 transition duration-500 ease-in-out p-0 text-center hover:bg-gray-500"><a class="text-center "> Home </a></li>
            <li class="md:px-6 md:py-2.5 transition duration-500 p-0 hover:bg-gray-500"><router-link to="about">Shop</router-link></li>
            <li class="md:px-6 md:py-2.5   transition duration-500 p-0 hover:bg-gray-500 relative">
                  <span class=" absolute inline-flex h-3 w-3 right-3  z-10 rounded-full bg-primary"></span>
                <a>Chart</a></li>
            <li class="md:px-6 transition duration-500 md:py-2.5 p-0 hover:bg-gray-500"><a>Article</a></li>
            
        </ul>
        <div class="hidden w-12/12 md:w-4-12 md:flex justify-end" ref="search">
          <div class="relative flex flex-wrap my-2 items-stretch mb-3">
            <span
              class="z-10 h-full leading-snug font-normal absolute text-center text-gray-400 absolute bg-transparent rounded text-base items-center justify-center w-8 p-2 pt-1.5">
              <svg class="text-primary stroke-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <input type="text" placeholder="search"
              class="px-3 py-0 w-36 placeholder-gray-400  text-black relative bg-white bg-white rounded text-xs shadow outline-none focus:outline-none focus:shadow-outline pl-10" />
          </div>
          <img alt="Vue logo" class="flex my-3 md:ml-10 md:mr-4" src="./../assets/img/profile.png">
        </div>
    </nav>
</template>
<script>
export default {
   name: 'Navbar',
   methods:{
        active(){
          this.$refs["mobileMenu"].classList.toggle('hidden')
           this.$refs["search"].classList.toggle('hidden')
       }
   },
}
</script>
<style>
 .active{
        display: block;
    }    

</style>
