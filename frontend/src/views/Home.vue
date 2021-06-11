<template>
  <div class="home pt-16 md:pt-0">
    <div class="flex flex-wrap flex-col-reverse md:flex-row">
      <div class="w-full md:w-5/12 p-0 md:pr-8">
        <VueSlickCarousel :arrows="true" :dots="false">
          <div>
            <img src="@/assets/img/1.png" alt="">
          </div>
          <div> <img src="@/assets/img/2.png" alt=""></div>
          <div> <img src="@/assets/img/3.png" alt=""></div>
          <div> <img src="@/assets/img/4.png" alt=""></div>
          <div> <img src="@/assets/img/5.png" alt=""></div>
          <div> <img src="@/assets/img/6.png" alt=""></div>

          <template #prevArrow>
            <div class="right-bot prev">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </div>
          </template>
          <template #nextArrow>
            <div class="right-bot next">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </div>
          </template>
        </VueSlickCarousel>
      </div>
      <div class="w-full md:w-7/12 p-5 relative">
        <p class="header text-6xl mt-0 md:mt-16">Humanize <br> The Virtual</p>
        <p class="w-full md:w-paragraph mt-10 font-normal">Lorem ipsum dolor sit amet, consectetur
          adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
          enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
          commodo consequat. Duis aute irure dolor in</p>
        <button
          class="border-primary mt-12 border rounded-xl p-3 transition duration-500 hover:bg-primary hover:rounded-xl hover:text-white px-16">Let's
          Go</button>
        <div class="absolute bottom-5 right-12 md:bottom-3 md:right-36 flex">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="-7 -2 24 24" width="30" height="30"
            preserveAspectRatio="xMinYMin" class="icon__icon">
            <path
              d="M2.046 3.865v2.748H.032v3.36h2.014v9.986H6.18V9.974h2.775s.26-1.611.386-3.373H6.197V4.303c0-.343.45-.805.896-.805h2.254V0H6.283c-4.34 0-4.237 3.363-4.237 3.865z">
            </path>
          </svg>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -4 24 24" width="30" height="30"
            preserveAspectRatio="xMinYMin" class="ml-3 icon__icon">
            <path
              d="M20 1.907a8.292 8.292 0 0 1-2.356.637A4.07 4.07 0 0 0 19.448.31a8.349 8.349 0 0 1-2.607.98A4.12 4.12 0 0 0 13.846.015c-2.266 0-4.103 1.81-4.103 4.04 0 .316.036.625.106.92A11.708 11.708 0 0 1 1.393.754a3.964 3.964 0 0 0-.554 2.03c0 1.403.724 2.64 1.824 3.363A4.151 4.151 0 0 1 .805 5.64v.05c0 1.958 1.415 3.591 3.29 3.963a4.216 4.216 0 0 1-1.08.141c-.265 0-.522-.025-.773-.075a4.098 4.098 0 0 0 3.832 2.807 8.312 8.312 0 0 1-5.095 1.727c-.332 0-.658-.02-.979-.056a11.727 11.727 0 0 0 6.289 1.818c7.547 0 11.673-6.157 11.673-11.496l-.014-.523A8.126 8.126 0 0 0 20 1.907z">
            </path>
          </svg>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 24 24" width="30" height="30"
            preserveAspectRatio="xMinYMin" class="ml-3 icon__icon">
            <path
              d="M14.017 0h-8.07A5.954 5.954 0 0 0 0 5.948v8.07a5.954 5.954 0 0 0 5.948 5.947h8.07a5.954 5.954 0 0 0 5.947-5.948v-8.07A5.954 5.954 0 0 0 14.017 0zm3.94 14.017a3.94 3.94 0 0 1-3.94 3.94h-8.07a3.94 3.94 0 0 1-3.939-3.94v-8.07a3.94 3.94 0 0 1 3.94-3.939h8.07a3.94 3.94 0 0 1 3.939 3.94v8.07z">
            </path>
            <path
              d="M9.982 4.819A5.17 5.17 0 0 0 4.82 9.982a5.17 5.17 0 0 0 5.163 5.164 5.17 5.17 0 0 0 5.164-5.164A5.17 5.17 0 0 0 9.982 4.82zm0 8.319a3.155 3.155 0 1 1 0-6.31 3.155 3.155 0 0 1 0 6.31z">
            </path>
            <circle cx="15.156" cy="4.858" r="1.237"></circle>
          </svg>
        </div>
      </div>
    </div>
    <div class="mt-28 text-center text-lg container mx-auto">
      <a @click="featured = true" class="mx-8">Featured</a>
      <a @click="featured = false" class="mx-8">New Arrivals</a>
      <transition name="fade" mode="out-in">
        <div class="w-full mx-auto" v-if="featured == true">
          <featured-carousel />
        </div>
        <div class="w-full" v-else-if="featured == false">
          <featured-carousel />
        </div>
      </transition>
    </div>
    <highlight-carousel class="mt-8" />
  </div>
</template>

<script>
// @ is an alias to /src
import VueSlickCarousel from 'vue-slick-carousel'
  import 'vue-slick-carousel/dist/vue-slick-carousel.css'
  // optional style for arrows & dots
  import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'
  import FeaturedCarousel from '@/components/FeaturedCarousel.vue';
    import HighlightCarousel from '@/components/HighlightCarousel.vue';

export default {
  name: 'Home',
  data(){
    return{
      featured: true
    } 
  },
  components: {
     VueSlickCarousel,
     FeaturedCarousel,
     HighlightCarousel,
  },
};
</script>
<style scoped lang="postcss">
.slick-prev, .slick-next {
   @apply rounded-lg;
  @apply w-10;
  @apply py-8;
  @apply h-10;
  @apply text-4xl;
  @apply border;
  @apply border-white;
  @apply hover:bg-primary;
  @apply hover:border-primary;
  @apply transition;
  @apply duration-300;
  @apply focus:outline-none;
  background-color: transparent;
  text-align: center;
  padding: 0;
  color: white;
  justify-content: center;
  align-items: center;
  border: 2px solid white;
  cursor: pointer;
  z-index: 3;
}

 .right-bot.next {
    top: unset;
    right: 0;
    transform: translate(0, 0);
    right: 20px;
    bottom: 85px;
  }
   .right-bot.prev {
     top: unset;
    left: unset;
    right:80px;
    transform: translate(0, 0);
    bottom: 85px;
  }

  .slick-next:before{
    content: '';
  }
    .slick-prev:before{
    content: '';
  }
</style>