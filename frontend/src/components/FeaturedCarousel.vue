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
      <div class="b">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
      </svg>
      </div>
    </template>
        <template #nextArrow>
      <div class="c">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
</svg>
      </div>
    </template>
       <template #customPaging>
      <div class="carousel-dot">
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
<style scoped lang="postcss">
.slick-prev, .slick-next {
   @apply rounded-lg;
  @apply w-10;
  @apply py-8;
  @apply h-10;
  @apply text-4xl;
  @apply border;
  @apply text-gray-400;
  @apply border-gray-300 !important;
  @apply hover:text-white;
  @apply hover:bg-primary;
  @apply hover:border-primary !important;
  @apply transition;
  @apply duration-300;
  @apply focus:outline-none;
  background-color: transparent;
  text-align: center;
  padding: 0;
  justify-content: center;
  align-items: center;
  border: 2px solid white;
  cursor: pointer;
  z-index: 3;
}

.slick-prev {
  @apply ml-8;
  }

  .slick-next {
    @apply mr-8
  }

  .slick-next:before{
    content: '';
  }
    .slick-prev:before{
    content: '';
  }
  .slick-active .carousel-dot{
  @apply bg-primary;
  @apply transition;
  @apply duration-700;
  @apply ease-in-out;
  }
  .carousel-dot{
    @apply bg-gray-400;
    @apply rounded-full;
     @apply transition;
  @apply duration-300;
    width: 15px;
    height: 15px;
  }
</style>