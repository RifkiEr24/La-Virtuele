<template>
  <div class="container mx-auto">
    <secondary-button
      btn-text='<span class="iconify" data-icon="bx:bxs-chevron-left" data-inline="false"></span>' />
    <div class="flex flex-wrap -mx-2 mt-10">
      <div class="w-full md:w-4/12 px-2 order-2 md:order-1">
        <h1 class="text-5xl font-bold header text-graysecondary tracking-wide">{{product.name}}</h1>
        <p class="text-primary  text-xl font-semibold">Rp {{product.price}}</p>
        <div class="info mt-20">
          <h2 class="text-3xl font-bold header  tracking-wide">Info</h2>
          <p class="mt-2 ">{{product.description}}</p>
        </div>
      </div>
      <div class="w-full md:w-4/12 px-2 order-1 md:order-2">
        <VueSlickCarousel v-if="product.gallery" ref="c1" :asNavFor="$refs.c2" :slidesToShow="1">
          <div v-for="image in product.gallery" :key="image.id">
            <inner-image-zoom :src="`https://la-virtuele.harizmunawar.repl.co${image.image}`"
              :zoomSrc="`https://la-virtuele.harizmunawar.repl.co${image.image}`" :zoomScale="0.1"
             />
          </div>
        </VueSlickCarousel>

        <VueSlickCarousel  v-if="product.gallery" ref="c2" :asNavFor="$refs.c1" :slidesToShow="3" :focusOnSelect="true"
          :draggable="false">
          <div v-for="image in product.gallery" :key="image.id">
            <img class="img-navigation"
              :src="`https://la-virtuele.harizmunawar.repl.co${image.image}`" alt="">
          </div>
        </VueSlickCarousel>
      </div>
      <div class="w-full md:w-4/12 px-2 order-3" >
        <div class=" w-full md:w-72  ml-0 md:ml-auto">
          <bordered-heading :heading-text="'Size'" />
          <label class="container my-3">S
            <input type="radio" name="size-select" checked="checked">
            <span class="checkmark"></span>
          </label>
          <label class="container my-3">M
            <input type="radio" name="size-select">
            <span class="checkmark"></span>
          </label>
          <label class="container my-3">X
            <input type="radio" name="size-select">
            <span class="checkmark"></span>
          </label>
          <label class="container my-3">XL
            <input type="radio" name="size-select">
            <span class="checkmark"></span>
          </label>
          <label class="container my-3">XXL
            <input type="radio" name="size-select">
            <span class="checkmark"></span>
          </label>
          <bordered-heading class="mt-10" :heading-text="'Quantity'" />
          <div class="quantity-counter flex gap-10 mt-3">
            <button @click="decrementCounter"
              class="bg-transparent border-2 border-black p-1 hover:bg-primary hover:border-primary hover:text-white transition duration-500"><span
                class="iconify" data-icon="bx:bxs-chevron-left" data-inline="false"></span></button>
            <span class="font-semibold">{{count}}</span>
            <button @click="incrementCounter"
              class="bg-transparent border-2 border-black p-1 hover:bg-primary hover:border-primary hover:text-white transition duration-500"><span
                class="iconify" data-icon="bx:bxs-chevron-right"
                data-inline="false"></span></button>
          </div>
          <secondary-button class="mt-5"
            btn-text='<span class="iconify inline" data-icon="bi:cart-plus" data-inline="false"></span> <span class="ml-3 p-4">add to cart</span>' />
        </div>
      </div>
    </div>
    <div class="review pb-10">
       <bordered-heading class="mt-10" :heading-text="'Review'" />
       <review-item class="my-8"/>
       
    </div>
  </div>
</template>

<script>
import SecondaryButton from '@/components/SecondaryButton.vue';
import InnerImageZoom from 'vue-inner-image-zoom';
import VueSlickCarousel from 'vue-slick-carousel'
import BorderedHeading from '@/components/BorderedHeading.vue'
import ReviewItem from '@/components/ReviewItem.vue'

import 'vue-inner-image-zoom/lib/vue-inner-image-zoom.css';

export default {
components: {
  VueSlickCarousel,
   SecondaryButton,
   ReviewItem,
   'inner-image-zoom': InnerImageZoom,
   BorderedHeading
  },
data(){
    return{
      product:{},
      count : 1
    }
  },
  methods: {
        incrementCounter: function() {
            this.count += 1;
        },
        decrementCounter: function() {
          if(this.count != 1){
             this.count -= 1;
          }
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

<style lang="postcss" scoped>
.iiz__btn{
  @apply bg-primary;
}
.img-navigation{

  height: 100px;
  object-fit: cover;
}
.container {
  display: block;
  position: relative;
  padding-left: 35px;
  font-size: 18px;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

/* Hide the browser's default checkbox */
.container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

/* Create a custom checkbox */
.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 25px;
  width: 25px;
  border: 2px solid black;
  background-color: transparent;
}

/* On mouse-over, add a grey background color */
.container:hover input ~ .checkmark {
}

/* When the checkbox is checked, add a blue background */
.container input:checked ~ .checkmark {
  @apply bg-primary;
  @apply border-primary;  
}

/* Create the checkmark/indicator (hidden when not checked) */
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

/* Show the checkmark when checked */
.container input:checked ~ .checkmark:after {
  display: block;
}

/* Style the checkmark/indicator */
.container .checkmark:after {
  left: 9px;
  top: 5px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
}
</style>