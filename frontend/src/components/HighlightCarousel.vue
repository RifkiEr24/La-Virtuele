<template>
  <VueSlickCarousel v-bind="settings" class="" ref="carousel">
    <div v-bind:style="{ backgroundImage: 'url('+require('@/assets/img/back.png')+')' }">
      <div class="flex flex-row z-10">
        <div class="w-6/12">
          <img src="@/assets/img/collapse1.png" class="mx-auto d-block" alt="">
          <div class="flex justify-center gap-52 pb-10">
            <button class="custom-prev" @click="showPrev">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <button class="custom-next" @click="showNext">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        <div class="w-6/12">
          <div class="bg-white my-20 rounded-l-lg p-10">
            <div class="flex flex-row justify-between">
              <div>
                <p class="text-4xl font-bold">Collapse</p>
                <p class="text-lg">Oversized T-Shirt</p>
              </div>
              <div>
                <p class="text-lg text-gray-500 line-through text-right">Rp.200.000</p>
                <div class="flex">
                  <img src="@/assets/img/teenyicons_discount-solid.png" class="w-8 h-8 my-auto"
                    alt="">
                  <p class="text-3xl ml-3">Rp.159.500</p>
                </div>

              </div>
            </div>
            <p class="text-lg font-semibold mt-6">Material : </p>
            <p class="bg-gray-300 bg-opacity-50 p-3 rounded-xl mt-3 font-medium">Cotton HISPANIC 200
              gsm (streetwear)</p>
            <p class="text-lg font-semibold mt-6">Size : </p>
            <div class="flex gap-3">
              <p class="bg-gray-300 bg-opacity-50 px-5 py-2 rounded-xl mt-3 font-medium">S</p>
              <p class="bg-gray-300 bg-opacity-50 px-5 py-2 rounded-xl mt-3 font-medium">M</p>
              <p class="bg-gray-300 bg-opacity-50 px-5 py-2 rounded-xl mt-3 font-medium">L</p>

            </div>
            <button
              class="border-primary mt-10 border text-white rounded-xl p-3 transition duration-500 bg-primary hover:rounded-xl hover:text-white px-16">Let's
              Add To Cart</button>
          </div>
        </div>
      </div>


    </div>
    <div v-bind:style="{ backgroundImage: 'url('+require('@/assets/img/back2.png')+')' }">
   <div class="flex flex-row z-10">
        <div class="w-6/12">
          <img src="@/assets/img/collapse2.png" class="mx-auto d-block" alt="">
          <div class="flex justify-center gap-52 pb-10">
            <button class="custom-prev" @click="showPrev">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </button>
            <button class="custom-next" @click="showNext">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                  clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        <div class="w-6/12">
          <div class="bg-white my-20 rounded-l-lg p-10">
            <div class="flex flex-row justify-between">
              <div>
                <p class="text-4xl font-bold">Collapse</p>
                <p class="text-lg">Oversized T-Shirt</p>
              </div>
              <div>
                <p class="text-lg text-gray-500 line-through text-right">Rp.200.000</p>
                <div class="flex">
                  <img src="@/assets/img/teenyicons_discount-solid.png" class="w-8 h-8 my-auto"
                    alt="">
                  <p class="text-3xl ml-3">Rp.159.500</p>
                </div>

              </div>
            </div>
            <p class="text-lg font-semibold mt-6">Material : </p>
            <p class="bg-gray-300 bg-opacity-50 p-3 rounded-xl mt-3 font-medium">Cotton HISPANIC 200
              gsm (streetwear)</p>
            <p class="text-lg font-semibold mt-6">Size : </p>
            <div class="flex gap-3">
              <p class="bg-gray-300 bg-opacity-50 px-5 py-2 rounded-xl mt-3 font-medium">S</p>
              <p class="bg-gray-300 bg-opacity-50 px-5 py-2 rounded-xl mt-3 font-medium">M</p>
              <p class="bg-gray-300 bg-opacity-50 px-5 py-2 rounded-xl mt-3 font-medium">L</p>

            </div>
            <button
              class="border-primary mt-10 border text-white rounded-xl p-3 transition duration-500 bg-primary hover:rounded-xl hover:text-white px-16">Let's
              Add To Cart</button>
          </div>
        </div>
      </div>
    </div>
    <template #prevArrow>
      <div class="b">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
          fill="currentColor">
          <path fill-rule="evenodd"
            d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
            clip-rule="evenodd" />
        </svg>
      </div>
    </template>
    <template #nextArrow>
      <div class="c">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20"
          fill="currentColor">
          <path fill-rule="evenodd"
            d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
            clip-rule="evenodd" />
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

export default {
  name: 'HighlightCarousel',
  data(){
    return{
      settings: {
          arrows: false,
          dots: false,
        },
    }
  },
   methods: {
      showNext() {
        this.$refs.carousel.next()
      },
      showPrev() {
        this.$refs.carousel.prev()
      },
    },
   components: {
   VueSlickCarousel    
  },
}
</script>
<style scoped lang="postcss">
.slick-prev, .slick-next, .custom-next, .custom-prev {
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

</style>