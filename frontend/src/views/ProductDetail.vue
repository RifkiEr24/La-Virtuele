<template>
  <div class="container mx-auto">
                  <secondary-button btn-text='<span class="iconify" data-icon="bx:bxs-chevron-left" data-inline="false"></span>' />

      <div class="flex -mx-2 mt-10">
          <div class="w-4/12 px-2">
            <h1 class="text-5xl font-bold header text-graysecondary tracking-wide">{{product.product}}</h1>
            <p class="text-primary  text-xl font-semibold">Rp {{product.price}}</p>
            <div class="info mt-20">
              <h2 class="text-3xl font-bold header  tracking-wide">Info</h2>
              <p class="mt-2 ">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in</p>
            </div>
          </div>
           <div class="w-4/12 px-2">
                <VueSlickCarousel
                ref="c1"
                :asNavFor="$refs.c2"
                :focusOnSelect="true">
                <div  v-for="image in product.gallery" :key="image.id">
                <inner-image-zoom  :src="`https://la-virtuele.harizmunawar.repl.co${image.image}`" :zoomScale=1	 :zoomType="'hover'" :hideHint="true"  />
                </div>
         

                /*...*/
              </VueSlickCarousel>

                <VueSlickCarousel
                ref="c2"
                :asNavFor="$refs.c1"
                :slidesToShow="3"
                :focusOnSelect="true">
                    <div  v-for="image in product.gallery" :key="image.id">
                      <img :src="`https://la-virtuele.harizmunawar.repl.co${image.image}`" alt="">
                </div>
                /*...*/
              </VueSlickCarousel>
          </div>
           <div class="w-4/12 px-2">
                b
          </div>
      </div>
      
  </div>
</template>

<script>
import SecondaryButton from '@/components/SecondaryButton.vue';
import InnerImageZoom from 'vue-inner-image-zoom';
import VueSlickCarousel from 'vue-slick-carousel'

import 'vue-inner-image-zoom/lib/vue-inner-image-zoom.css';

export default {
components: {
  VueSlickCarousel,
   SecondaryButton,
   'inner-image-zoom': InnerImageZoom
  },
data(){
    return{
      product:{}
    }
  },
  created(){
      this.axios.get(`http://la-virtuele.harizmunawar.repl.co/api/v1/products/${this.$route.params.id}/`).then((response) => {
        this.product=response.data;
        console.log(this.product);
      })
  },
}
</script>

<style>

</style>