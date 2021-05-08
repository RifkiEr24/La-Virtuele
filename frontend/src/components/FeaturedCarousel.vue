<template>
     <VueSlickCarousel v-bind="settings"  class="">
      <div>  <img class="mx-auto" src="@/assets/img/cloth1.png" alt=""></div>
      <div> <img  class="mx-auto" src="@/assets/img/cloth2.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth3.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth4.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth5.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth6.png" alt=""></div>
        <div>  <img class="mx-auto" src="@/assets/img/cloth1.png" alt=""></div>
      <div> <img  class="mx-auto" src="@/assets/img/cloth2.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth3.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth4.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth5.png" alt=""></div>
      <div> <img class="mx-auto" src="@/assets/img/cloth6.png" alt=""></div>
      <template #prevArrow>
      <div class="right-bot prev">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      </div>
    </template>
        <template #nextArrow>
      <div class="right-bot next">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
</svg>
      </div>
    </template>
    </VueSlickCarousel>
</template>
<script>
// @ is an alias to /src
import VueSlickCarousel from 'vue-slick-carousel'
  import 'vue-slick-carousel/dist/vue-slick-carousel.css'
  // optional style for arrows & dots
  import 'vue-slick-carousel/dist/vue-slick-carousel-theme.css'
export default {
  name: 'FeaturedCarousel',
  data(){
    return{
      settings: {
          arrows: true,
          dots: true,
          rows:2,
          slidesToShow:3,
          slidesPerRow:1,
          slidesToScroll:3,	
          centerPadding	:'0px'
        },
    }
  },
   components: {
   VueSlickCarousel    
  },
}
</script>