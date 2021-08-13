<template>
  <VueSlickCarousel :arrows="true" :dots="false">
    <div>
      <img src="@/assets/img/1.png"  class="w-full" alt="">
    </div>
    <div> <img src="@/assets/img/2.png"  class="w-full" alt=""></div>
    <div> <img src="@/assets/img/3.png"  class="w-full" alt=""></div>
    <div> <img src="@/assets/img/4.png"  class="w-full" alt=""></div>
    <div> <img src="@/assets/img/5.png"  class="w-full" alt=""></div>
    <div> <img src="@/assets/img/6.png"  class="w-full" alt=""></div>

    <template #prevArrow>
      <button class="right-bot prev">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
          fill="currentColor">
          <path fill-rule="evenodd"
            d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
            clip-rule="evenodd" />
        </svg>
      </button>
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
</template>

<script>
import VueSlickCarousel from 'vue-slick-carousel'

  
export default {
   components: {
   VueSlickCarousel    
  },
}
</script>

<style scoped lang="postcss">
.slick-prev, .slick-next {
  @apply w-10;
  @apply py-8;
  @apply h-10;
  @apply text-4xl;
  @apply border;
  @apply bg-white;
  @apply text-black;
  @apply border-white;
  @apply hover:bg-primary;
  @apply hover:border-primary;
  @apply transition;
  @apply duration-300;
  @apply hover:text-white;

  text-align: center;
  padding: 0;
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
    right: 0;
    bottom: 5px;
  }
   .right-bot.prev {
     top: unset;
    left: unset;
    right:40px;
    transform: translate(0, 0);
    bottom: 5px;
  }

  .slick-next:before{
    content: '';
  }
    .slick-prev:before{
    content: '';
  }
</style>